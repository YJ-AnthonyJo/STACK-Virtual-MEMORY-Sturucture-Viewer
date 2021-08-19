import config as C
import os, atexit

try:
    import readline
except ImportError:
    #!pip install pyreadline
    import pyreadline as readline

import sys

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
    def print_(substitution, *args):
        suggestion = args[1]
        Cmd_first_Word = [i.split()[0] for i in suggestion]
        count = [Cmd_first_Word.count(i) for i in sorted(set(Cmd_first_Word))]
        #print('\n|-----Suggestion-----|', flush = True)
        print()
        c = 0
        for value in count:
            print(*[i.rstrip() for i in suggestion[c:value+c]], sep = ' / ', flush = True)
            c += value
        print(f'> {args[0]}', end = '', flush = True) #어떻게 가능한지는 모르겠지만, {args[0]}에 해당하는 부분은 backspace로 지울 수 있네.. ({args[0]} 대신 p를 넣어도 가능하다.. input함수와 어떻게 완만한 합의를 했나보다.. 추측할 수 밖에없다.)

def CMD_Alters(text):
    options = [i.strip() for i in C.commands if i.startswith(text.split()[0])]
    if len(options):
        return options
    else:
        return []


def signal_handler():
    # your code here
    try: 
        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print ('\nTerminate')
        sys.exit(1)
    #sys.exit(0)

def getCMD():
    #입력값 처리 #1 : 기본 처리
    try:
        CMD = input('> ')
        CMD = CMD.strip() # 좌우 공백 제거.
        if CMD == '': return False # 입력값이 없을 때. #return False -> continue
        
        #입력값 처리 #2 : 대안 선택 및 표시
        alters = CMD_Alters(CMD) #가능한 대안 가져오기.
        if len(alters) == 1:
            if ' ' in CMD:
                CMD = alters[0] + CMD[CMD.index(' '):]
            else:
                CMD = alters[0]
            return CMD
        else:
            print(*alters if len(alters) != 0 else ['Command Not Found\nAvailable Command :']+C.commands, sep=' ')
            return False #return False -> continue
    except KeyboardInterrupt:
        signal_handler()
    except EOFError:
        print("Invalid Input, Mabye typed CTRL + D")

def init():
    if os.path.isfile('./.STACK_Viewer_history'):
        readline.read_history_file('./.STACK_Viewer_history')
    atexit.register(readline.write_history_file, './.STACK_Viewer_history')

    completer = Completer(C.commands + C.extra)
    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer.complete)
    readline.set_completion_display_matches_hook(completer.print_)
    readline.set_completer_delims(';')
    # ;을 기준으로 복수개의 명령 제공.
    # bash의 경우 두번째 인자는 무조건 파일로 인식하는 듯하다.
    # git의 경우, 명령어에 따라서 자동완성기능을 다르게 제공한다.
    # git  -> 다음 명령어들
    # git branch -> 브랜치 들.