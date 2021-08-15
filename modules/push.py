import re
from Func import *
import config as C

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
    p = re.compile(r'push \$(.+)= *[\'\"](.*)[\'\"] *(\d*)') 
    m = p.match(C.CMD)
    if m: # for push {$vari1} {=} {'"문자열"'} {#byte}
        var = m.group(1).strip()
        #변수명 valid여부 체크
        if not chk_valid_variable_name(var):
            return
        
        data_string = m.group(2)
        
        byte = m.group(3)
        byte = int(byte) if byte != '' else len(data_string)
        if var in C.VARIABLES:
            print("This Variable name is already exist, please use other.")
            return
        C.VARIABLES[var] = data_string[:byte]
    else:
        p = re.compile(r'push +[\'\"](.*)[\'\"] *(\d*)') # for push {'"문자열"'} {#byte}
        m = p.match(C.CMD)
        if bool(m): 
            var = ''
            data_string = m.group(1)
            
            byte = m.group(2)
            byte = int(byte) if byte != '' else len(data_string)
        else:
            print(inspect.cleandoc("""Syntax Error! See valid syntax using help(push)
                  if you evaluate your expression are rigth, please add issue AT 
                       https://github.com/YJ-AnthonyJo/STACK-Virtual-MEMORY-Sturucture-Viewer/issues/"""))
            return
    """
    STACK = [
        {'assignedVar': str,
        'RelativeDistance(base: EBP, RBP)': int,
        'RelativeDistance(base: ESP, RSP)': int,
        'dataLength' : int}
    ]
    """
    # C.STACK.append( [var, data_string[:byte] , byte ] )
    C.STACK.append({
        'assignedVar' : var, # 해당 데이터에 접근할 수 있는 변수 이름.(string형태)
        'RDistance(BP)' : Calc_RDistance(byte, 'RDistance(BP)'), # EBP, RSP에서 현 데이터가 떨어진 거리.
        'RDistance(SP)' : Calc_RDistance(byte, 'RDistance(SP)'), # ESP, ESP에서 현 데이터가 떨어진 거리.
        'DLength' : byte # 해당 데이터가 가진 크기.
    })