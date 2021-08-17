from Func import *
import config as C
import re
def push():
    '''
    USEAGE
    1. push {$vari1}{=}{'문자열'} {#byte} #이후 set등으로 접근 가능.
    2. push {'문자열'} {#byte}
    
    {$vari1} : vari는 파이썬 변수 생성 규칙 만족해야한다.(정규식으로는 아래과 같다.)
        p_chk_vari = re.compile("^[a-zA-Z_$ㄱ-ㅎ가-힣ㅏ-ㅣ][\wㄱ-ㅎ가-힣ㅏ-ㅣ$]*$")
    {'문자열'} : data에 해당한다.
    {#byte} : 기본값 = 문자열 길이, 값 존재하면 해당 byte만큼만 잘라서 할당.
    
    return값
    None
    ''' 
    # push {$var1} {#byte}
    # push {$var1} {=} {'"문자열"'} {#byte}
    # push {$var1} {=} {$var2} {#byte}
    m = re.match(r'push +\$(.+)', C.CMD)
    if m:
        # 변수명 check안해주어도 됨. (이미 var로 존재한다는 것은 통과했다는 것.)
        var = m.group(1) #$var = {'"data"'} {#length}일 때, $이후 부분을 가져감. 후처리.
        if '=' not in var : 
            # push {$var} :$var은 assigned된 상태여야한다.
            _, data_string, var, byte = push_var_only(var)
        else:
            # push {$var1} {=} {'"문자열"'} {#byte}
            _, data_string, var, byte = push_var_new_assignment(var)
        
        if not _: 
            ErrMsg('push')
            return
        
    else: # push {'"data"'} {#byte}으로 간주.
        _, var, data_string, byte = push_data()
        if not _: # push {'"data"'} {#byte}도 아니라면..
            ErrMsg('push')
            return


    C.STACK.append({
        'data' : data_string,
        'assignedVar' : var, # 해당 데이터에 접근할 수 있는 변수 이름.(string형태)
        'RDistance(BP)' : Calc_RDistance(byte), # EBP, RSP에서 현 데이터가 떨어진 거리.
        'DLength' : byte # 해당 데이터가 가진 크기.
    })
    chk_sfp(data_string if var == '' else C.VARIABLES[var]['data'])

def push_var_only(var):
    m = re.match('(.+) +(\d+)', var)
    if m: # push $var {length}
        var = m.group(1)
        byte = int(m.group(2))
    else: # push $var
        var = var.strip()
        byte = C.VARIABLES[var]['DLen']
    
    if not chk_var_in_VARIABLES(True, var) : return [False] * 4
    
    data_string, var = LWS(byte, var)
    
    return True, data_string, var, byte

def push_var_new_assignment(var):
    # var 새로 assignment.
    m = re.match(r'(.+)= *[\'\"](.*)[\'\"] *(\d*)', var) 
    if m: 
        var = m.group(1).strip()
        if not chk_valid_variable_name(var):
            return [False] * 4
        
        data_string = m.group(2)
        
        byte = m.group(3)
        byte = int(byte) if byte != '' else len(data_string)
        
        data_string = data_string[:byte]
        
        C.VARIABLES[var] = {
            'type' : 'STACKLink',
            'data' : data_string,
            'DLen' : byte
        }
        data_string = '' # LWS : C.VARIABLES의 data로 접근할 것임.(동기화 위해)
        return True, data_string, var, byte
    else : #var : 't2 = $t1'
        m = re.match(r'(.+)= *\$(.+)', var) 
        if m:
            l_var = m.group(1).strip()
            if not chk_valid_variable_name(l_var):
                return [False] * 4
            r_var = m.group(2).strip()
            
            m = re.match(r'(.+) +(\d+)', r_var)
            if m:
                r_var = m.group(1)
                if not chk_var_in_VARIABLES(True, r_var): return [False] * 4
                byte = int(m.group(2))
            else:
                r_var = r_var
                if not chk_var_in_VARIABLES(True, r_var): return [False] * 4
                byte = C.VARIABLES[r_var]['DLen']
            
            C.VARIABLES[l_var] = {
                'type' : 'STACKLink',
                'data' : C.VARIABLES[r_var]['data'][:byte],
                'DLen' : byte
            }
            data_string = ''
            return True, data_string, l_var, byte
        else: 
            return [False] * 4

def push_data():
    m = re.match(r'push +[\'\"](.*)[\'\"] *(\d*)', C.CMD) 
    if m: 
        var = ''
        data_string = m.group(1)
        
        byte = m.group(2)
        byte = int(byte) if byte != '' else len(data_string)
        
        data_string = data_string[:byte]
        return True, var, data_string, byte
    else:
        return [False] * 4