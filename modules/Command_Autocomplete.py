import config as C

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

def CMD_Alters(text):
    options = [i for i in C.commands if i.startswith(text.split()[0])]
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

def init():
    #입력값 처리 #1 : 기본 처리
    try:
        completer = Completer(C.commands)
        readline.parse_and_bind('tab: complete')
        readline.set_completer(completer.complete)
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