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
        m = re.match(r'pop +modify +\$(.+)', C.CMD)
        m1 = re.match(r'pop +new +\$(.+)', C.CMD)
        if m or m1:
            var = m.group(1) if m else m1.group(1)
            
            chk = chk_var_in_VARIABLES(True, var) if m else chk_var_in_VARIABLES(False, var) and chk_valid_variable_name(var)
            if not chk : return
            
            data = C.STACK.pop()
            C.VARIABLES[var] = {
                'type' : 'var',
                'data' : C.VARIABLES[data['assignedVar']] if data['assignedVar'] != '' else data['data'],
                'DLen' : len(data['data'])
            }
            print(var, '=', C.VARIABLES[var]['data'])
        
            chk_sfp(C.VARIABLES[var]['data'])
            pass
        else:
            ErrMsg('pop')