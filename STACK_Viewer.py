import re, os
from typing import Dict
import inspect
try:
    import readline
except ImportError:
    #!pip install pyreadline
    import pyreadline as readline

'''입력값 처리 부분 #start'''
class Completer(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None
commands = ["print", "push", "pop", "set", "clear", 'quit']
completer = Completer(commands)
readline.parse_and_bind('tab: complete')    
readline.set_completer(completer.complete)
def CMD_Alters(text):
    options = [i for i in commands if i.startswith(text.split()[0])]
    if len(options):
        return options
    else:
        return []
'''입력값 처리 부분 #end'''



def print_stack(STACK):
    """
    push값 중, sfp가 없으면, 가장 처음 push된 주소를 sfp라고 지정.
    (즉, sfp가 해당 push된 데이터 위에 존재하고 있다고 판단.)
    """
    #issue 10번 수정 : variable namd이 있는 경우 variable name을 출력.
    if len(STACK) == 0:
        print("STACK is Empty.")
        return
    print_data = lambda _: (_[1] if _[0] == '' else '$' + _[0]) # issue 10, variable_name이 있으면 variable_name, 없으면 data
    length = max([len( print_data(_) ) for _ in STACK ]) #한 줄에 출력해야할 가장 긴 것의 길이 가져옴.
    
    max_length = length if length < 20 else 20 #한줄에 출력할 최대 글자.
    
    SUM = str(sum( [_[2] for _ in STACK] )) # ebp뒤에 나올 최대 숫자 -> 문자열화 길이.
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
    for idx, data in enumerate(STACK):
        if data[1] in ['sfp', 'SFP']:
            ebp = idx
    
    
    #4바이트를 1줄로 하여 출력
    #5바이트인 경우, 2줄이다.
    #너무 긴 경우, ...으로 대체;
    #한줄 최대 출력 : 20자
    for idx, _ in enumerate(STACK):
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
            tmp = sum( [_[2] for _ in STACK[ ebp + (1 if ebp==-1 else 0) : idx + 1] if _[1] not in ('sfp', 'SFP')])
            if tmp !=0 :
                print(f' <= EBP - {tmp}', end='')
        print()
        print('-'* (max_length + 4), end='')
    #print('-' * (length + 4 + len(SUM) + 4) ) 
    print(f"\n{'*'* (max_length//2 + len(SUM)//2 + 5) } STACK {'*'* (max_length//2 + len(SUM)//2 + 5)}")

def push(CMD):
    
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
    m = p.match(CMD)
    if bool(m): 
        vari = m.group(1).strip()
        
        #변수명 valid여부 체크
        p = re.compile("^[a-zA-Z_$ㄱ-ㅎ가-힣ㅏ-ㅣ][\wㄱ-ㅎ가-힣ㅏ-ㅣ$]*$")
        if not bool(p.match(vari)):
            print(inspect.cleandoc("""Syntax Error! : Invalid Variable name
                                    Check valid Variable name by help(varialbe_name)
                                    if you evaluate your expression are rigth, please add issue AT 
                                       https://github.com/YJ-AnthonyJo/STACK-Virtual-MEMORY-Sturucture-Viewer/issues/"""))
            return
        
        data_string = m.group(2)
        
        byte = m.group(3)
        byte = int(byte) if byte != '' else len(data_string)
        if vari in VARIABLES:
            print("This Variable name is already exist, please use other.")
            return
        VARIABLES[vari] = data_string[:byte]
    else:
        p = re.compile(r'push +[\'\"](.*)[\'\"] *(\d*)') # for push {'"문자열"'} {#byte}
        m = p.match(CMD)
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
    STACK.append( [vari, data_string[:byte] , byte ] )
    
    
    '''기존, update전
        USEAGE
        push data bytes=len(data) #기본값
        만일 data에 공백 등이 섞여있고 data의 마지막이 숫자로 끝난다면 $$를 붙여주어야한다.
        
        push 안녕 123$$ -> 안녕 123이 들어감.
        push 안녕 123$$
        push 안녕 alex -> 안녕 alex가 들어감.
        
        만약 123$$가 데이터이면 어떻게하지.. -> $하나 더 붙이기.
    '''
    ''' CMD = CMD[5:] # 'push '이후의 문자열
        
        match = lambda p,x=CMD: bool(p.match(x)) # 함수 설정.
        
        p = re.compile('^ *.+ +[0-9]+$')
        if match(p): 
            #마지막 공백이후가 byte를 나타내는 것이라면
            _ = CMD.split()[-1]
            byte = int(_)
            CMD = CMD[:-len(_)-1]
            
        else: # 기본byte : 문자열의 길이.
            p = re.compile('[0-9]+\\$\\$$')
            if bool( p.match(CMD.split()[-1]) ): #마지막이 숫자로 끝나는 경우.
                CMD = CMD[:-2]
            p = re.compile('[0-9]+\\$\\$\\$$')
            if bool( p.match(CMD.split()[-1]) ): #마지막이 숫자로 끝나는 경우.
                CMD = CMD[:-1]
            byte = len(CMD)
    '''

def set_(CMD):
    '''
    \{\} : 실제로 들어가는 string에서의 {}을 의미.
    ###set###
    
    #1 variable : $사용하기.
        set {$vari_name}={data || $vari_name} {#length}
        * {$vari_name} : 사용할 변수 이름. 공백 자동 제거(rstrip)
        * {data || $vari_name} 
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
    
    p_chk_vari = re.compile("^[a-zA-Z_$ㄱ-ㅎ가-힣ㅏ-ㅣ][\wㄱ-ㅎ가-힣ㅏ-ㅣ$]*$")
    
    p = re.compile(r'set (\$.+)= *(\$.+)') # for $vari1 = $vari2 {#length}
    m = p.match(CMD)
    if bool(m): 
        vari1, vari2 = [m.group(i).rstrip()[1:] for i in [1,2]] # $variables_name -> variables_name
        return
    
    p = re.compile(r'set (\$.+)=(.+)') # for $vari1 = data #data는 따옴표안에 공간 이름에 담는 것 따로 두기.
    m = p.match(CMD)
    if bool(m):
        vari1 = m.group(1).rstrip()[1:]; data = m.group(2) #$vari_name -> vari_name && data
        return
    


STACK = list() # [ ['{vari}', '{data}', {byte}], ...]
VARIABLES = dict()
idx_of_vari_tmp = 0


while True: 
    #입력값 처리 #1 : 기본 처리
    CMD = input('> ')
    CMD = CMD.strip() # 좌우 공백 제거.
    if CMD == '': continue # 입력값이 없을 때.
    
    #입력값 처리 #2 : 대안 선택 및 표시
    alters = CMD_Alters(CMD) #가능한 대안 가져오기.
    if len(alters) == 1:
        if ' ' in CMD:
            CMD = alters[0] + CMD[CMD.index(' '):]
        else:
            CMD = alters[0]
    else:
        print(*alters if len(alters) != 0 else ['Command Not Found\nAvailable Command :']+commands, sep=' ')
        continue
    
    
    #입력값 처리 #3 : 명령어 구조에 맞게 처리.
    match = lambda p,x=CMD: bool(p.match(x)) # 함수 설정.
    
    p = re.compile('print.*')
    if match(p) : #stack 출력(범위 지정기능), 변수 출력, STACK의 데이터 출력.(구현해야)
        '''
        print all : 모든 변수 정보 출력
        print vari_name : vari_name에 해당하는 변수 정보 출력.
        print 0:3 => 0~3째 스택데이터를 보여라.
        '''
        if CMD == 'print': #STACK출력
            print_stack(STACK)
        elif CMD == 'print all': #모든 변수 출력
            for name, data in VARIABLES.items():
                print(name, '=', data)

        else:
            p = re.compile('print +(\d*):(\d*)$')
            m = p.match(CMD)
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
                    from_, to = [int(from_), int(to)]
                print(f"print {from_ if from_ != None else ''} : {to if to != None else ''}")
                print_stack(STACK[ from_ : to ])

            else: 
                #변수출력.
                p = re.compile('print +\$(.+)')
                m = p.match(CMD)
                if bool(m):
                    vari = m.group(1).strip()
                    p = re.compile("^[a-zA-Z_$ㄱ-ㅎ가-힣ㅏ-ㅣ][\wㄱ-ㅎ가-힣ㅏ-ㅣ$]*$")
                    if not bool(p.match(vari)):
                        print(inspect.cleandoc("""Syntax Error! : Invalid Variable name
                                Check valid Variable name by help(varialbe_name)
                                if you evaluate your expression are rigth, please add issue AT 
                                https://github.com/YJ-AnthonyJo/STACK-Virtual-MEMORY-Sturucture-Viewer/issues/"""))
                    else:
                        print(vari, '=' , VARIABLES[vari])
                else:
                    print("Err : Invalid Parameter")
                """
                원코드
                elif ' ' in CMD and not match(re.compile('print +.*:.*$')): # parameter에 :가 포함되지 않았을 경우. -> 변수 출력.
                    _ =  ''.join(CMD.split()[1:])
                    if _ in VARIABLES:
                        print(_, '=' , VARIABLES[_])
                    else:
                        print(f"Can't Find {_}")
                """
        continue #아래 if문 통과.
    
    p = re.compile('push .+')
    if match(p): #push구현.
        push(CMD)
        continue #아래 if문 통과.
    
    p = re.compile('pop.*')
    if match(p) : # pop구현.
        if len(STACK) == 0:
            print("Empty STACK")
            continue 
        
        CMD = CMD.split()
        if len(CMD) == 1: #parm이 주어지지 않았을 때, 즉 pop만하고 버릴 때.
            STACK.pop()
        else: #parm이 주어졌을 때.
            #아래 두 if => 변수명으로 사용 불가능한 것 필터링.
            if CMD[1] == 'all': #all필터링.
                print(f"You can't use all as variable name, temporary stored in tmp_{idx_of_vari_tmp}")
                VARIABLES[f'tmp_{idx_of_vari_tmp}'] = STACK.pop()
                print(f'tmp_{idx_of_vari_tmp} =', VARIABLES[f"tmp_{idx_of_vari_tmp}"])
                idx_of_vari_tmp += 1
                continue
            if match(re.compile('\d*:\d*$'), CMD[1]): #{:}, {숫자:숫자} 필터링.
                print(f"You can't use : in variable name temporary stored in tmp_{idx_of_vari_tmp}")
                VARIABLES[f'tmp_{idx_of_vari_tmp}'] = STACK.pop()
                print(f'tmp_{idx_of_vari_tmp} =', VARIABLES[f"tmp_{idx_of_vari_tmp}"])
                idx_of_vari_tmp += 1
                continue
            #필터링 통과했을 때, VARIABLES에 pop된 값 저장.
            VARIABLES[CMD[1]] = STACK.pop()
            print(CMD[1], '=', VARIABLES[CMD[1]])
            #본래 실제 변수로 설정하고자 했으나, 여러 사정으로 dictionary로 바꿈.(편리성..)
            # try:
            #     exec(f'{CMD[1]} = {STACK.pop()};VARIABLES.append("{CMD[1]}")')
            #     print(CMD[1], '=', eval(CMD[1]))
            # except:
            #     print(f"Syntax Error : Possible variable name is not available. temporary stored in tmp{idx_of_vari_tmp}")
            #     print(f"tmp{idx_of_vari_tmp}", '=', eval(f"tmp{idx_of_vari_tmp}"))
            continue #아래 if문 통과.
    
    p = re.compile('set .+')
    if match(p) : #스택에 끼워넣기, 변수 바꾸기
        set_(CMD)
        continue #아래 if문 통과.
    
    if CMD == 'clear': # 화면 지우기.
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')
        continue #아래 if문 통과.

    if CMD == 'quit' :
        break