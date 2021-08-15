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
        if bool(m): #범위지정 STACK출력 숫자(혹은 공백):숫자(혹은 공백) 의 경우만 실행됨.
            from_ , to = [m.group(i) for i in [1,2]]
            if from_ == '':
                if to == '': #parm이 { : } 일 때
                    from_, to = [None] * 2
                else: 
                    from_, to = [None, int(to)] #parm이 {:숫자} 일 때
            elif to == '': #parm이 {숫자:}일 때
                from_, to = [int(from_), None]
            else: #parm이 {숫자:숫자}일 때
                range_ = {'from': int(from_), 'to': int(to)}
            print(f"print {from_ if from_ != None else ''} : {to if to != None else ''}")
            print_stack(range_)

        else: 
            #변수출력.
            p = re.compile('print +\$(.+)')
            m = p.match(C.CMD)
            if bool(m):
                vari = m.group(1).strip()
                if chk_valid_variable_name(vari):
                    print(vari, '=' , C.VARIABLES[vari])
            else:
                print("Err : Invalid Parameter")


def print_stack(range_ = {'from': None, 'to' : None}):
    if len(C.STACK) == 0:
        print("STACK is Empty.")
        return
    print_data = lambda data: (data['data'] if data['assignedVar'] == '' else '$' + data['assignedVar']) # issue 10, variable_name이 있으면 variable_name, 없으면 data
    length = max([len( print_data(data) ) for data in C.STACK ]) #한 줄에 출력해야할 가장 긴 것의 길이 가져옴.
    
    max_length = length if length < 20 else 20 #한줄에 출력할 최대 글자.
    
    SUM = str(max( [data['RDistance(BP)'] for data in C.STACK] )) # EBP뒤에 나올 최대 숫자 -> 문자열화 길이.
    
    print(f"\n{'*'* (max_length//2 + len(SUM)//2 + 5) } STACK {'*'* (max_length//2 + len(SUM)//2 + 5)}")
    '''
        # | data | <= EBP - num
        # max_length for len(data)
        # max_length for indent
        # len(SUM) for num
        # 4 for <= EBP
    '''
    '''
        #4바이트를 1줄로 하여 출력
        #5바이트인 경우, 2줄이다.
        #너무 긴 경우, ...으로 대체;
        #한줄 최대 출력 : 20자
    '''
    for data in C.STACK:
        len_of_line = data['DLength'] // 4 + int(data['DLength'] % 4 != 0) #현 데이터당 출력 줄수 지정.
        for _ in range(1, len_of_line):
            print("| ", end='')
            print(' ' * len( print_data(data) ), end=' ' * (length-len( print_data(data) )))
            print(' |')
        print('|', print_data(data), end=' ' * ( max_length-len(print_data(data)) ))
        
        sign = 1 if data["RDistance(BP)"] >= 0 else 0
        Rdist = format(data['RDistance(BP)'], '+d')[1:]
        if Rdist == '0':
            print(f' | <= EBP')
        else:
            print(f' | <= EBP {"+" if sign else "-"} {Rdist}')
        
        print('-'* (max_length + 4))
    print(f"\n{'*'* (max_length//2 + len(SUM)//2 + 5) } STACK {'*'* (max_length//2 + len(SUM)//2 + 5)}")