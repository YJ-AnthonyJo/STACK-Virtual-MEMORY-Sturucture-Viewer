import re, os
import config as C
from Func import *
from _print_Func import *

def init():
    '''
    print all : 모든 변수 정보 출력
    print var_name : var_name에 해당하는 변수 정보 출력.
    print 0:3 => 0~3째 스택데이터를 보여라.
    '''
    if C.CMD == 'print': #STACK출력
        print_stack()
        return
    
    if re.match('print +all$', C.CMD): #모든 변수 출력
        for name, data in C.VARIABLES.__dict__.items():
            print(f'${name}', '=', data)
        return

    m = re.match(r'print +(\d*):(\d*)$', C.CMD)
    if m: #범위지정 STACK출력 숫자(혹은 공백):숫자(혹은 공백) 의 경우만 실행됨.
        from_ , to = [m.group(i) for i in [1,2]]
        if from_ == '':
            if to == '': #parm이 { : } 일 때
                from_, to = [None] * 2
            else: 
                from_, to = [None, int(to)] #parm이 {:숫자} 일 때
        elif to == '': #parm이 {숫자:}일 때
            from_, to = [int(from_), None]
        else: #parm이 {숫자:숫자}일 때
            from_, to = [int(from_), int(to)]
        print_stack(from_, to)
        print(f"print {from_ if from_ != None else ''} : {to if to != None else ''}")
        return

    #변수출력.
    m = re.match(r'print +\$([^ ]+)$', C.CMD)
    if m:
        vari = m.group(1)
        print(f"${vari}", '=' , C.VARIABLES[vari])
        return
    
    m = re.match('print +env +\$([^ ]+)', C.CMD)
    if m:
        env = m.group(1)
        if env in C.EnvVar:
            print(C.EnvVar[env])
        else:
            print("No such environmental variable. please 'print env all' to check all env")
        return
    
    m = re.match('print +env +all$', C.CMD)
    if m:
        print("*****ENVIRONMENTAL VARIABLES*****")
        for name, value in C.EnvVar.items():
            print(f'${name}', '=', value)
        return
            
    ErrMsg('print')
            


def print_stack(from_ = None, to = None):
    if len(C.STACK) == 0:
        print("STACK is Empty.")
        return
    
    try:
        max_length = os.get_terminal_size()[0] #현재 terminal에서 최대로 출력가능한 값.
    except:
        # print("Can't get current window size. Mabye Running on IDLE.\nThat's OK. Just little inconvenience.😅")
        print("경고 : 창 크기를 받아올 수 없음.")
        max_length = None
    
    default = 4 + 10 # | hello | <= EBP - 5에서 data, num부분 뺀 default 출력부. # 4는 |까지 부분. 10은 이후.
    
    PrintData = lambda data: (data['data'] if data['assignedVar'] == '' else '$' + data['assignedVar']) # issue 10, variable_name이 있으면 variable_name, 없으면 data
    
    _ = get_max(
        lambda d : len(PrintData(d))
    )#한 줄에 출력해야할 가장 긴 data의 길이.
    
    maxNum = get_max(
        lambda d : len(
                str(d['RDistance_BP']) [0 if d['RDistance_BP'] >= 0 else 1 : ]
            )
    ) # EBP뒤에 나올 최대 숫자 -> 문자열화 길이.
    
    maxLen = default + _ + maxNum # 왜 가운데 이모티콘 같지 ㅋㅋㅋㅋㅋ (+_+)!!!
    
    if max_length != None:
        maxLen = maxLen if maxLen < max_length else max_length #한줄에 출력할 최대 글자.
    else: # 위 except에서 말한 Just Little inconvenience에 해당하는 부분..
        maxLen = maxLen
    
    maxDataLen = maxLen - default - maxNum
    maxDataLen = _ if _ < maxDataLen else maxDataLen # data만 따졌을 때 출력할 수 있는 최대.
    
    numOfStars = (maxLen-7) // 2 + (maxLen-7) % 2
    print(f"{'*' *  numOfStars} STACK {'*' * numOfStars}")
    print('-' * (maxDataLen + 4)) # |부분까지.
    for idx, data in enumerate(C.STACK[from_ : to]):
        if C.EnvVar['MultiLineP'] == 'Yes':
            print_stack_v2(data, maxDataLen, PrintData, idx) # 복수 줄에 출력.
        else: print_stack_v1(data,maxDataLen, PrintData, idx) #.....으로 치환.

    print(f"{'*' * numOfStars } STACK {'*' * numOfStars}")