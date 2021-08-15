import config as C
from Func import *
def init():
    '''
    print all : 모든 변수 정보 출력
    print vari_name : vari_name에 해당하는 변수 정보 출력.
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
    """
    push값 중, sfp가 없으면, 가장 처음 push된 주소를 sfp라고 지정.
    (즉, sfp가 해당 push된 데이터 위에 존재하고 있다고 판단.)
    """
    #issue 10번 수정 : variable namd이 있는 경우 variable name을 출력.
    if len(C.STACK) == 0:
        print("STACK is Empty.")
        return
    print_data = lambda _: (_[1] if _[0] == '' else '$' + _[0]) # issue 10, variable_name이 있으면 variable_name, 없으면 data
    length = max([len( print_data(_) ) for _ in C.STACK ]) #한 줄에 출력해야할 가장 긴 것의 길이 가져옴.
    
    max_length = length if length < 20 else 20 #한줄에 출력할 최대 글자.
    
    SUM = str(sum( [_[2] for _ in C.STACK] )) # ebp뒤에 나올 최대 숫자 -> 문자열화 길이.
    #str(SUM) #3+1+1+1+ len(str(SUM))
    print(f"\n{'*'* (max_length//2 + len(SUM)//2 + 5) } STACK {'*'* (max_length//2 + len(SUM)//2 + 5)}", end='')
    #print('-' * (length + 4 + len(SUM) + 4), end='' ) 
    
    # | data | <= EBP - num
    # max_length for len(data)
    # max_length for indent
    # len(SUM) for num
    # 4 for <= EBP
    
    # find sfp(SFP) #가장 마지막을 기준으로 함.
    ebp = -1
    for idx, data in enumerate(C.STACK):
        if data[1] in ['sfp', 'SFP']:
            ebp = idx
    
    
    #4바이트를 1줄로 하여 출력
    #5바이트인 경우, 2줄이다.
    #너무 긴 경우, ...으로 대체;
    #한줄 최대 출력 : 20자
    for idx, _ in enumerate(C.STACK):
        #_[0]은 variable_name
        #_[1]은 data
        #_[2]은, bytes
        len_of_line = _[2] // 4 + int(_[2] % 4 != 0) #현 데이터당 출력 줄수 지정.
        if len(_[0]) > max_length: #len_of_line을 넘지 않게 분할 출력이 필요. 21~40까지는 절반씩 출력.
            #만일, len_of_line의 글자를 다 채웠는데도 다 출력못하는 경우는 ...으로 나머지 출력.
            #...으로 출력할지 전체 다 출력할지 parm으로 지정해주기(해야할것.)
            pass
        for _1 in range(1, len_of_line + 1): #data 출력부 _1은, 현 데이터의 출력 줄
            print('\n| ', end='')
            if _1 == len_of_line: #마지막에 한번에 몰아서 출력. ->바꾸어야.
                #print((_[1] if _[0]=='' else '$'+_[0]), end=' ' * (max_length-len((_[1] if _[0]=='' else '$'+_[0]))))
                print(print_data(_), end=' ' * (max_length-len( print_data(_) )) )
                
            else:
                print(' ' * len( print_data(_) ), end=' ' * (length-len( print_data(_) )))
            print(' |', end='')
        
        if idx == ebp: #EBP 출력부
            print(f' <= EBP', end='')
        else:
            tmp = sum( [_[2] for _ in C.STACK[ ebp + (1 if ebp==-1 else 0) : idx + 1] if _[1] not in ('sfp', 'SFP')])
            if tmp !=0 :
                print(f' <= EBP - {tmp}', end='')
        print()
        print('-'* (max_length + 4), end='')
    #print('-' * (length + 4 + len(SUM) + 4) ) 
    print(f"\n{'*'* (max_length//2 + len(SUM)//2 + 5) } STACK {'*'* (max_length//2 + len(SUM)//2 + 5)}")