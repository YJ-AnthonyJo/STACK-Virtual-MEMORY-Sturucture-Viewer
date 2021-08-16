from pyreadline import rlmain
import config as C
from Func import *
import re

def _set_():
    '''
        \\{\\} : 실제로 들어가는 string에서의 {}을 의미.
        ###set###
        
        #1 variable : $사용하기.
            set {$var_name}={data || $var_name} {#length}
            * {$var_name} : 사용할 변수 이름. 공백 자동 제거(rstrip)
            * {data || $var_name} 
                * data : 공백 없이 들어가야한다.
                * $vari_name : $다음에 들어가는 이름(공백 자동 제거(rstrip))
            * {#length}
                * parm2 == $vari_name : 옮길 데이터 바이트 수. 생략시, 변수 전체 데이터
                * parm2 == data : 할당할 데이터 크기, push와 동일한 작동기준.
            
        #2 istack : ebp기준의 상대주소 사용.
            set \{{length}\}{#ebp esp}-{num}={data}
            * {length} : 수식, 변수($사용) 허용.
            * {#ebp} : 기본값이 ebp(생략가능), esp 사용가능.
            * {num} : ebp로 부터 얼마나 떨어져있는지.
            * {data} : 공백 없이 들어가야한다.
            
            명령 입력 후, 적용 결과를 임시로 보여주며(print) 진행할 것인지 확인.
    '''
    "set new"
    # set new $vari1 = $vari2 {#length}
    p = re.compile(r'set +new +\$(.+)= *\$(.+)') 
    m = p.match(C.CMD)
    if m: 
        var1, var2 = [m.group(i).rstrip() for i in [1,2]]
        
        p = re.compile(r'(.+) +(\d+)')
        m = p.match(var2)
        if bool(m):
            var2 = m.group(1)
            byte = int(m.group(2))
        else:
            byte = len(C.VARIABLES[var2])
        
        if not chk_valid_variable_name(var1, var2): return #변수명 확인.
        
        
        if var1 in C.VARIABLES: #기존에 존재시.
            print("This Variable name is already exist, please use other.")
            return
        else:
            C.VARIABLES[var1] = C.VARIABLES[var2][:byte]
        return
    
    # set new $vari1 = 'data' {#length}
    p = re.compile(r'set +new +\$(.+)= *[\'\"](.*)[\'\"] *(\d*)') 
    m = p.match(C.CMD)
    if bool(m):
        var1 = m.group(1).rstrip() 
        if not chk_valid_variable_name(var1): return
        data = m.group(2)
        byte = m.group(3)
        byte = int(byte) if byte != '' else len(data)
        
        if var1 in C.VARIABLES:
            print("This Variable name is already exist, please use other.")
            return
        C.VARIABLES[var1] = data[:byte]
        return
    
    # set new #ebp-num = $vari2 {#length}
    p = re.compile(r'set +new +(.*)([-+]\d+) *= *\$(.+)') 
    m = p.match(C.CMD)
    if bool(m): 
        #기준 정하기. esp? ebp?
        base = m.group(1)
        base = base if base != '' else 'ebp'
        
        #상대주소 +num, -num
        relativeAddr = int(m.group(2)) 
        
        
        #변수명, byte 받기.
        var = m.group(3)
        p = re.compile(r'(.+) +(\d+)')
        m = p.match(var)
        if bool(m):
            var = m.group(1)
            byte = int(m.group(2))
            pass
        else:
            byte = len(C.VARIABLES[var])
        if not chk_valid_variable_name(var): return #변수명 확인.
        
        
        
        """STACK = [
        {'assignedVar': str,
        'RDistance(BP)': int,
        'DLength' : int}
        ]"""
        idx = next( (index for (index, d) in enumerate(C.STACK) if d["RDistance(BP)"] == relativeAddr), None)
        if idx != None:
            C.STACK.insert(idx, {
                'data' : C.VARIABLES[var][:byte],
                'assignedVar' : var,
                'RDistance(BP)' : relativeAddr,
                'DLength' : byte
            })
            reset_RDistance_BP()
        else:
            print("relative address is invalid.") # ISSUE #21
        
        return
        
    # set new #ebp-num = 'data' {#length}
    p = re.compile(r'set +new +(.*)([-+]\d+) *= *[\'\"](.*)[\'\"] *(\d*)') 
    m = p.match(C.CMD)
    if bool(m):
        #기준 정하기. esp? ebp?
        base = m.group(1)
        base = base if base != '' else 'ebp'
        
        #상대주소 +num, -num
        relativeAddr = int(m.group(2)) 
        
        #데이터 입력받기.
        data = m.group(3)
        
        #byte받기.
        byte = m.group(4)
        byte = int(byte) if byte != '' else len(data)
        
        idx = next( (index for (index, d) in enumerate(C.STACK) if d["RDistance(BP)"] == relativeAddr), None)
        if idx != None:
            C.STACK.insert(idx, {
                'data' : data[:byte],
                'assignedVar' : '',
                'RDistance(BP)' : relativeAddr,
                'DLength' : byte
            })
            reset_RDistance_BP()
        else:
            print("relative address is invalid.") # ISSUE #21

        return

    "set"
    # set $var1 = $var2 {#length}
    p = re.compile(r'set +\$(.+)= *\$(.+)')
    m = p.match(C.CMD)
    if bool(m):
        var1, var2 = [m.group(i).rstrip() for i in [1,2]]
        
        p = re.compile(r'(.+) +(\d+)')
        m = p.match(var2)
        if bool(m):
            var2 = m.group(1)
            byte = int(m.group(2))
        else:
            byte = len(C.VARIABLES[var2])
        
        if not chk_valid_variable_name(var1, var2): return #변수명 확인.
        
        if var1 not in C.VARIABLES:
            print("This Variable name is not declared, please declare it first using set new")
        else:
            C.VARIABLES[var1] = C.VARIABLES[var2][:byte]            
        return
    
    # set $var1 = 'data' {#length}
    p = re.compile(r'set +\$(.+)= *[\'\"](.*)[\'\"] *(\d*)') 
    m = p.match(C.CMD)
    if bool(m):
        var1 = m.group(1).rstrip() 
        if not chk_valid_variable_name(var1): return
        data = m.group(2)
        byte = m.group(3)
        byte = int(byte) if byte != '' else len(data)
        
        if var1 not in C.VARIABLES:
            print("This Variable name is not declared, please declare it first using set new")
        else:
            C.VARIABLES[var1] = data[:byte]
        return
    
    # set #ebp-num = $var1 {#length}
    p = re.compile(r'set +(.*)([-+]\d+) *= *\$(.+)') 
    m = p.match(C.CMD)
    if bool(m):
        #기준 정하기. esp? ebp?
        base = m.group(1)
        base = base if base != '' else 'ebp'
        
        #상대주소 +num, -num
        relativeAddr = int(m.group(2))
        
        
        #변수명 받기.
        var = m.group(3)
        p = re.compile(r'(.+) +(\d+)')
        m = p.match(var)
        if bool(m):
            var = m.group(1)
            byte = int(m.group(2))
            pass
        else:
            byte = len(C.VARIABLES[var])
        if not chk_valid_variable_name(var): return #변수명 확인.
        
        
        idx = next( (index for (index, d) in enumerate(C.STACK) if d["RDistance(BP)"] == relativeAddr), None)
        if idx != None:
            C.STACK.insert(idx, {
                'data' : C.VARIABLES[var][:byte],
                'assignedVar' : var,
                'RDistance(BP)' : relativeAddr,
                'DLength' : byte
            })
            reset_RDistance_BP()
        else:
            print("relative address is invalid.") # ISSUE #21
        return
    
    # set #ebp-num = 'data' {#length}
    p = re.compile(r'set +(.*)([-+]\d+) *= *[\'\"](.*)[\'\"] *(\d*)') 
    m = p.match(C.CMD)
    if bool(m):
        #기준 정하기. esp? ebp?
        base = m.group(1)
        base = base if base != '' else 'ebp'
        
        #상대주소 +num, -num
        #지금은 +가 구현안되어있기에 -를 기준으로 구현.
        relativeAddr = - int(m.group(2)) #+구현시 int앞의 -빼고 다른 조건 넣어서 처리해주기.
        
        #데이터 입력받기.
        data = m.group(3)
        
        #byte받기.
        byte = m.group(4)
        byte = int(byte) if byte != '' else len(data)
        
        idx = next( (index for (index, d) in enumerate(C.STACK) if d["RDistance(BP)"] == relativeAddr), None)
        if idx != None:
            C.STACK.insert(idx, {
                'data' : data[:byte],
                'assignedVar' : '',
                'RDistance(BP)' : relativeAddr,
                'DLength' : byte
            })
            reset_RDistance_BP()
        else:
            print("relative address is invalid.") # ISSUE #21
        return