import config as C
import re
from Func import *

def pop():
    if len(C.STACK) == 0:
        print("Empty STACK")
        return
    
    m = re.match('^pop$', C.CMD)
    if m:
        data = C.STACK.pop()
        chk_sfp(data['data'])
        return
    
    m = re.match(r'pop +modify +\$([^ ]+)', C.CMD)
    if m:
        var = m.group(1)
        tmp = C.STACK.pop()
        C.VARIABLES[var] = C.var(data=tmp.data, DLen=tmp.DLen, type_='var')
        print('<<<pop결과>>>')
        print(var, '=', C.VARIABLES[var].data, '\n')
        return
    
    m = re.match(r'pop +new +\$([^ ]+)', C.CMD)
    if m:
        var = m.group(1)
        tmp = C.STACK.pop()
        C.VARIABLES.new(
            key=var, 
            item=C.var(data=tmp.data, DLen=tmp.DLen, type_='var')
        )
        print('<<<pop결과>>>')
        print(var, '=', C.VARIABLES[var].data, '\n')
        return
    
    ErrMsg('pop')