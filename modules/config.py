# config.py
from collections import UserDict, UserList
import inspect
import re
from modules.Func import Calc_RDistance
class stack(object):
    def __init__(s, 
                 data :str = '',
                 assignedVar :str = '',
                 DLen :int = None,
                 RDistance_BP :int = None,
                 type_:type = None
                 ):
        s.data : str = data
        s.assignedVar : str = assignedVar
        s.RDistance_BP : int = Calc_RDistance(DLen) if RDistance_BP == None else RDistance_BP
        s.DLen : int =  DLen
        s.type : type = type_
    def __setitem__(self, key, item):
        if key in self.__dict__:
            self.__dict__[key] = item
        else: raise KeyError(key+'는 stack의 Attribute가 아닙니다.')
    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else: raise KeyError("'" + key + "'" + '는 stack의 Attribute가 아닙니다.')

class STACK_(UserList):
    def append(self, item):
        if isinstance(item, stack):
            super().append(item)
    
    def indexA(self, target, target_data):
            return list(
                filter(
                        lambda x: STACK[x][target] == target_data, range(len(STACK))
                        )
                )
    def __getitem__(self, i) -> (stack):
        return super().__getitem__(i)
        
    

class var(object):
    def __init__(s, 
                 data :str = '', 
                 DLen :int = None, 
                 type_ :type = None
                 ):
        s.data : str = data
        s.DLen : int = DLen
        s.type : type = type_
    def __setitem__(self, key, item):
        if key in self.__dict__: self.__dict__[key] = item
        else: raise KeyError(key+'는 var의 Attribute가 아닙니다.')
    def __getitem__(self, key):
        if key in self.__dict__: return self.__dict__[key]
        else: raise KeyError("'" + key + "'" + '는 var의 Attribute가 아닙니다.')

class VARIABLES_(object): #UserDict
    def __setitem__(self, key, item:var) -> (None):
        '''변수 수정(modify)'''
        if key in self.__dict__:
            if isinstance(item, var):
                self.__dict__[key] = item
            else:
                print('VARIABLES의 value는 var의 Instance이어야 합니다.')
                #raise ValueError('r-value가 var의 Instance가 아닙니다.')
                raise ValueError
        else: 
            print(f'정의되지 않은 변수 : {key}')
            #raise KeyError(key+'는 VARIABLE_의 attribute가 아닙니다.')
            raise KeyError

    def __getitem__(self, key:var) -> (var):
        '''변수 참조(read)'''
        if key in self.__dict__:
            return self.__dict__[key]
        else: 
            print(f'정의되지 않은 변수 : {key}')
            #raise KeyError(key+'는 VARIABLE_의 attribute가 아닙니다.')
            raise KeyError

    def new(self, key, item:var) -> (None):
        '''변수 할당(assignment)'''
        if key not in self.__dict__:
            if isinstance(item, var):
                if not bool(re.match("^[a-zA-Z_$ㄱ-ㅎ가-힣ㅏ-ㅣ][\wㄱ-ㅎ가-힣ㅏ-ㅣ$]*$", key)):
                    print("올바르지 않은 변수이름")
                    raise KeyError
                else:
                    self.__dict__[key] = item
            else:
                print('VARIABLES의 value는 var의 Instance이어야 합니다.')
                raise ValueError
        else: 
            print('이미 존재하는 변수 :', key)
            raise KeyError
            



STACK = STACK_()
stack_ = stack()
"""
STACK = [
    data : stack
]
"""


VARIABLES = VARIABLES_()
"""
VARIABLES = {
    'varName' : (data : var)
    ...
}

- VARIABLES의 type은 치역의 개념이다.
- stack의 assignedvar가 정의역개념이고.
- assignedvar -> type.
- 따라서 복수개의 STACK 데이터가 하나의 variable에 대입될 수 있다.

# Default Var
- int_max, int_min 등.. boundary값.

"""


Cmd_Extended = [
    'print env ', 'print env all', 'print all', 'push new ', 'push modify ',\
    'pop new ', 'pop modify ', 'set new ', 'set modify ', 'set env '
    ]
commands = ["print ", "push ", "pop ", "set ", "clear ", 'quit ', 'delete ', 'save ', 'load ']

CMD = ''

EnvVar = {
    "MultiLineP" : "Yes", # 문자열. 'Yes' or 'No'
    "regType" : 32, # 정수. 32 or 64
    "Base" : "BP"
}