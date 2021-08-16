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
    # set new $var1 = $var2 {#length}
    # set new $var1 = 'data' {#length}
    m = re.match(r'set +new +\$(.+)= *(.+)', C.CMD)
    if m:
        var1 = m.group(1).rstrip()
        if not chk_valid_variable_name(var1) : return
        
        # set new $var1 = $var2 {#length}
        m1 = re.match(r'\$(.+)', m.group(2))
        if m1:
            var2 = m1.group(1).rstrip()
            var2, byte = set_var_and_byte(var2)
            if not chk_valid_variable_name(var2): return #변수명 확인.
            data = C.VARIABLES[var2][:byte]
        
        # set new $var1 = 'data' {#length}
        m1 = re.match(r'[\'\"](.*)[\'\"] *(\d*)', m.group(2)) 
        if m1:
            data = m1.group(1)
            byte = m1.group(2)
            byte = int(byte) if byte != '' else len(data)
            data = data[:byte]
        
        if var1 in C.VARIABLES: #기존에 존재시.
            print("This Variable name is already exist, please use other.")
            return
        C.VARIABLES[var1] = data
        return
    
    # set new #ebp-num = $var2 {#length}
    # set new #ebp-num = 'data' {#length}
    m = re.match(r'set +new +(.*)([-+]\d+) *= *(.+)', C.CMD)
    if m:
        #기준 정하기. esp? ebp?
        base = m.group(1)
        base = base if base != '' else 'ebp'
        
        #상대주소 +num, -num
        relativeAddr = int(m.group(2)) 
        
        # set new #ebp-num = $var2 {#length}
        m1 = re.match(r'\$(.+)', m.group(3)) 
        if m1: 
            #변수명, byte 받기.
            var = m1.group(1)
            var, byte = set_var_and_byte(var)
            if not chk_valid_variable_name(var): return #변수명 확인.

            data = C.VARIABLES[var][:byte]
        
        # set new #ebp-num = 'data' {#length}
        m1 = re.match(r'[\'\"](.*)[\'\"] *(\d*)', m.group(3)) 
        if m1:
            #데이터 입력받기.
            data = m1.group(1)
            
            #byte받기.
            byte = m1.group(2)
            byte = int(byte) if byte != '' else len(data)
            
            data = data[:byte]
            var = ''

        idx = next( (index for (index, d) in enumerate(C.STACK) if d["RDistance(BP)"] == relativeAddr), None)
        if idx != None:
            C.STACK.insert(idx, {
                'data' : data,
                'assignedVar' : var,
                'RDistance(BP)' : relativeAddr,
                'DLength' : byte
            })
            reset_RDistance_BP()
        else:
            print("relative address is invalid.") # ISSUE #21
        return

    "set"
    # set $var1 = $var2 {#length}
    # set $var1 = 'data' {#length}
    m = re.match(r'set +\$(.+)= *(.+)', C.CMD)
    if m:
        var1 = m.group(1).rstrip()
        if not chk_valid_variable_name(var1) : return
        
        # set $var1 = $var2 {#length}
        m1 = re.match(r'\$(.+)', m.group(2))
        if m1:
            var2 = m1.group(1).rstrip()
            var2, byte = set_var_and_byte(var2)
            if not chk_valid_variable_name(var2) : return
            data = C.VARIABLES[var2][:byte]
        
        # set $var1 = 'data' {#length}
        m1 = re.match(r'[\'\"](.*)[\'\"] *(\d*)', m.group(2))
        if m1:
            data = m1.group(1)
            byte = m1.group(2)
            byte = int(byte) if byte != '' else len(data)
            data = data[:byte]
        
        if var1 not in C.VARIABLES:
            print("This Variable name is not declared, please declare it first using set new")
            return
        C.VARIABLES[var1] = data
        return
    
    # set #ebp-num = $var1 {#length}
    # set #ebp-num = 'data' {#length}
    m = re.match(r'set +(.*)([-+]\d+) *= *(.+)', C.CMD) 
    if m:
        #기준 정하기. esp? ebp?
        base = m.group(1)
        base = base if base != '' else 'ebp'
        
        #상대주소 +num, -num
        relativeAddr = int(m.group(2))
        
        # set #ebp-num = $var1 {#length}
        m1 = re.match(r'\$(.+)', m.group(3)) 
        if m1:
            #변수명 받기.
            var = m1.group(1)
            var, byte = set_var_and_byte(var)
            if not chk_valid_variable_name(var): return #변수명 확인.  
            
            data = C.VARIABLES[var][:byte]
        
        # set #ebp-num = 'data' {#length}
        m1 = re.match('[\'\"](.*)[\'\"] *(\d*)', m.group(3))
        if m1:
            #데이터 입력받기.
            data = m1.group(1)
        
            #byte받기.    
            byte = m1.group(2)
            byte = int(byte) if byte != '' else len(data)
            
            data = data[:byte]
            var = ''
        
        
        idx = next( (index for (index, d) in enumerate(C.STACK) if d["RDistance(BP)"] == relativeAddr), None)
        if idx != None:
            C.STACK[idx] = {
                'data' : data,
                'assignedVar' : var,
                'RDistance(BP)' : relativeAddr,
                'DLength' : byte
            }
            reset_RDistance_BP()
        else:
            print("relative address is invalid.") # ISSUE #21
        return
    ErrMsg('set')