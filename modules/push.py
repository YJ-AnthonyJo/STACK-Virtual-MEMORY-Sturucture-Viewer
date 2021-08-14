import re
from Func import *
import config as C

def push():
    
    '''
    USEAGE ##New docsting!!
    1. push {$vari1}{=}{'문자열'} {#byte} #이후 set등으로 접근 가능.
    2. push {'문자열'} {#byte}
    
    {$vari1} : vari는 파이썬 변수 생성 규칙 만족해야한다.(정규식으로는 아래과 같다.)
        p_chk_vari = re.compile("^[a-zA-Z_$ㄱ-ㅎ가-힣ㅏ-ㅣ][\wㄱ-ㅎ가-힣ㅏ-ㅣ$]*$")
    {'문자열'} : data에 해당한다.
    {#byte} : 기본값 = 문자열 길이, 값 존재하면 해당 byte만큼만 잘라서 할당.
    '''    
    p = re.compile(r'push \$(.+)= *[\'\"](.*)[\'\"] *(\d*)') # for push {$vari1} {=} {'"문자열"'} {#byte}
    m = p.match(C.CMD)
    if bool(m): 
        vari = m.group(1).strip()
        
        #변수명 valid여부 체크
        if not chk_valid_variable_name(vari):
            return
        
        data_string = m.group(2)
        
        byte = m.group(3)
        byte = int(byte) if byte != '' else len(data_string)
        if vari in C.VARIABLES:
            print("This Variable name is already exist, please use other.")
            return
        C.VARIABLES[vari] = data_string[:byte]
    else:
        p = re.compile(r'push +[\'\"](.*)[\'\"] *(\d*)') # for push {'"문자열"'} {#byte}
        m = p.match(C.CMD)
        if bool(m): 
            vari = ''
            data_string = m.group(1)
            
            byte = m.group(2)
            byte = int(byte) if byte != '' else len(data_string)
        else:
            print(inspect.cleandoc("""Syntax Error! See valid syntax using help(push)
                  if you evaluate your expression are rigth, please add issue AT 
                       https://github.com/YJ-AnthonyJo/STACK-Virtual-MEMORY-Sturucture-Viewer/issues/"""))
            return
    C.STACK.append( [vari, data_string[:byte] , byte ] )