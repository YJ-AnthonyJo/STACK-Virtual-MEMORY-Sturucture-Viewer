import config as C
import re
from Func import *

def pop():
    if len(C.STACK) == 0:
            print("Empty STACK")
            return
    
    m = re.match('^pop$')
    if m:
        data = C.STACK.pop()
        chk_sfp(data['data'])
    else: #pop 결과를 변수에 저장 -> link with stack 아님.
        m = re.match(r'pop +\$(.+)')
        if m:
            var = m.group(1)
            if not chk_valid_variable_name(var):
                return
            
            data = C.STACK.pop()
            C.VARIABLES[C.CMD[1]] = {
                'type' : 'var',
                'data' : data['data'],
                'DLen' : len(data['data'])
            }
            print(C.CMD[1], '=', C.VARIABLES[C.CMD[1]]['data'])
        
            chk_sfp(C.VARIABLES[C.CMD[1]]['data'])
        else:
            ErrMsg('pop')