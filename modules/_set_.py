import config as C
from Func import *
import re

def _set_():
    r'''
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
            set \\{{length}\\}{#ebp esp}-{num}={data}
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
        '''init'''
        l_var, r_value = init_set_var(m)
        if not chk_valid_variable_name(l_var) : return
        if not chk_var_in_VARIABLES(False, l_var): return
        
        '''Case'''
        # set new $var1 = $var2 {#length}
        _, data, byte = case_set_var_1(r_value)
        
        # set new $var1 = 'data' {#length}
        _, data, byte = case_set_var_2(r_value)
        
        if not _ :
            ErrMsg('set')
            return
        
        '''Adjust to C.VARIABLES'''
        C.VARIABLES[l_var] = {
            'type' : 'var',
            'data' : data,
            'DLen' : byte
        }
        return
    
    # set new #ebp-num = $var2 {#length}
    # set new #ebp-num = 'data' {#length}
    m = re.match(r'set +new +(.*)([-+]\d+) *= *(.+)', C.CMD)
    if m:
        '''init'''
        base, relativeAddr, r_value = init_set_STACK(m)
        
        '''Case'''
        # set new #ebp-num = $var2 {#length}
        _, data, var, byte = case_set_STACK_1(r_value)
        
        # set new #ebp-num = 'data' {#length}
        _, data, var, byte = case_set_STACK_2(r_value)
        
        if not _ :
            ErrMsg('set')
            return

        '''Adjust to STACK'''
        adjust_set_STACK(True, data, var, relativeAddr, byte)
        return

    "set"
    # set $var1 = $var2 {#length}
    # set $var1 = 'data' {#length}
    m = re.match(r'set +\$(.+)= *(.+)', C.CMD)
    if m:
        '''init'''
        l_var, r_value = init_set_var(m)
        if not chk_valid_variable_name(l_var) : return
        if not chk_var_in_VARIABLES(True, l_var): return
        
        '''Case'''
        # set $var1 = $var2 {#length}
        _, data, byte = case_set_var_1(r_value)
        
        # set $var1 = 'data' {#length}
        _, data, byte = case_set_var_2(r_value)
        
        if not _ :
            ErrMsg('set')
            return
        
        '''Adjust to C.VARIABLES'''
        C.VARIABLES[l_var]['data'] = data
        C.VARIABLES[l_var]['DLen'] = byte
        if C.VARIABLES[l_var]['type'] == 'STACKLink':
            idx = next( (index for (index, d) in enumerate(C.STACK) if d["assignedVar"] == l_var), None)
            if idx != None :
                C.STACK[idx]['DLength'] = byte
                reset_RDistance_BP()
        return
    
    # set #ebp-num = $var1 {#length}
    # set #ebp-num = 'data' {#length}
    m = re.match(r'set +(.*)([-+]\d+) *= *(.+)', C.CMD) 
    if m:
        '''init'''
        base, relativeAddr, r_value = init_set_STACK(m)
        
        '''Case'''
        # set #ebp-num = $var1 {#length}
        _, data, var, byte = case_set_STACK_1(r_value)
        
        # set #ebp-num = 'data' {#length}
        _, data, var, byte = case_set_STACK_2(r_value)
        
        if not _ :
            ErrMsg('set')
            return
        
        '''Adjust to C.STACK'''
        adjust_set_STACK(False, data, var, relativeAddr, byte)
        return
    ErrMsg('set')