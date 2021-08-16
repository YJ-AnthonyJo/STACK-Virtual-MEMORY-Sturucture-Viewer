import re
import config as C
from Func import *
def init():
    '''
    print all : 모든 변수 정보 출력
    print var_name : var_name에 해당하는 변수 정보 출력.
    print 0:3 => 0~3째 스택데이터를 보여라.
    '''
    if C.CMD == 'print': #STACK출력
        print_stack()
    elif C.CMD == 'print all': #모든 변수 출력
        for name, data in C.VARIABLES.items():
            print(name, '=', data)

    else:
        p = re.compile('print +(\d*):(\d*)$')
        m = p.match(C.CMD)
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

        else: 
            #변수출력.
            p = re.compile('print +\$(.+)')
            m = p.match(C.CMD)
            if bool(m):
                vari = m.group(1).strip()
                if chk_valid_variable_name(vari):
                    print(vari, '=' , C.VARIABLES[vari])
            else:
                ErrMsg('print')


def print_stack(from_ = None, to = None):
    if len(C.STACK) == 0:
        print("STACK is Empty.")
        return
    PrintData = lambda data: (data['data'] if data['assignedVar'] == '' else '$' + data['assignedVar']) # issue 10, variable_name이 있으면 variable_name, 없으면 data
    
    _ = get_max(
        lambda d : len(PrintData(d))
    )#한 줄에 출력해야할 가장 긴 것의 길이 가져옴.
    maxLen = _ if _ < 20 else 20 #한줄에 출력할 최대 글자.
    
    maxNum = get_max(
        lambda d : len(
                str(d['RDistance(BP)']) [0 if d['RDistance(BP)'] >= 0 else 1 : ]
            )
    ) # EBP뒤에 나올 최대 숫자 -> 문자열화 길이.
    
    numOfStars = maxLen//2 + maxNum//2 + 5
    print(f"{'*' *  numOfStars} STACK {'*' * numOfStars}")
    print('-' * (maxLen + 4))
    for data in C.STACK[from_ : to]:
        LineNum = data['DLength'] // 4 + int(data['DLength'] % 4 != 0) #현 데이터당 출력 줄수 지정.
        
        for _ in range(1, LineNum): print("|", ' ' * maxLen, '|') # 마지막 줄 전까지 공백 출력.
        PData = PrintData(data)
        print('|', PData, ' '*(maxLen-len(PData)), end='') # 마지막 줄에 데이터 출력.
        
        sign = 1 if data["RDistance(BP)"] >= 0 else 0 #양수여부.
        if data['RDistance(BP)'] == 0: print(f'| <= EBP')
        else: print(f'| <= EBP {"+" if sign else "-"} {str(data["RDistance(BP)"])[0 if sign else 1:]}') #| <= EBP - N //OR// | <= EBP + N
        
        print('-' * (maxLen + 4))
    print(f"{'*' * numOfStars } STACK {'*' * numOfStars}")