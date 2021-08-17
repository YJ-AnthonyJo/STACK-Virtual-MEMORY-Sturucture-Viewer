import config as C
import re
from Func import *

def pop():
    if len(C.STACK) == 0:
        print("Empty STACK")
        return
    
    m = re.match('^pop$', C.CMD)
    if m: # pop만 수행.
        data = C.STACK.pop()
        chk_sfp(data['data'])
    else: # pop 결과를 변수에 저장 -> link with stack 아님.
        m = re.match(r'pop +\$(.+)', C.CMD)
        if m:
            var = m.group(1)
            if not chk_valid_variable_name(var):
                return
            
            data = C.STACK.pop()
            C.VARIABLES[var] = {
                'type' : 'var',
                'data' : data['data'],
                'DLen' : len(data['data'])
            }
            print(var, '=', C.VARIABLES[var]['data'])
        
            chk_sfp(C.VARIABLES[var]['data'])
        else:
            ErrMsg('pop')