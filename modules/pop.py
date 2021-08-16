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
    else:
        m = re.match(r'pop +\$(.+)')
        if m:
            var = m.group(1)
            if not chk_valid_variable_name(var):
                return
            
            C.VARIABLES[C.CMD[1]] = C.STACK.pop()
            print(C.CMD[1], '=', C.VARIABLES[C.CMD[1]])
        
            chk_sfp(C.VARIABLES[C.CMD[1]]['data'])
        else:
            ErrMsg('pop')