from Func import *
import config as C
import re
from push_Func import *

def push(): 
    # push {$var1} {byte}
    m = re.match(r'^push +\$(.+) +(\d+)$', C.CMD)
    if m:
        var = m.group(1)
        byte = int(m.group(2))
        if byte >= C.VARIABLES[var].DLen:
            C.STACK.append(
                C.stack(data='', assignedVar=var, DLen=byte)
            )
        else:
            C.STACK.append(
                C.stack(data=C.VARIABLES[var].data[:byte], 
                        assignedVar='', DLen=byte)
            )
        return
    
    # push {$var1}
    m = re.match(r'push +\$([^ ]+)$', C.CMD)
    if m:
        var = m.group(1)
        byte = C.VARIABLES[var].DLen
        C.STACK.append(
            C.stack(data='', assignedVar=var, DLen=byte)
        )
    
    # push modify {$var1} {=} {'"문자열"'} {byte}
    m = re.match(r'push +modify +\$([^ ]+) *= *([\'\"])(.*)\2 +(\d+)$', C.CMD)
    if m:
        var = m.group(1)
        data = m.group(3)
        byte = int(m.group(4))
        
        push_modify_var_assign(data, byte, var)
        return
    
    # push modify {$var1} {=} {'"문자열"'}
    m = re.match(r'push +modify +\$([^ ]+) *= *([\'\"])(.*)\2$', C.CMD)
    if m:
        var = m.group(1)
        data = m.group(3)
        byte = len(data)
        
        push_modify_var_assign(data, byte, var)
        return
    
    # push modify {$var1} {=} {$var2} {byte}
    m = re.match(r'push +\$([^ ]+) *= *\$([^ ]) +(\d+)$', C.CMD)
    if m :
        lvar = m.group(1)
        rvar = m.group(2)
        byte = int(m.group(3))
        push_modify_var_assign(C.VARIABLES[rvar].data[:byte], byte, lvar)
        return
    
    # push modify {$var1} {=} {$var2}
    m = re.match(r'push +\$([^ ]+) *= *\$([^ ])$', C.CMD)
    if m :
        lvar = m.group(1)
        data = C.VARIABLES[m.group(2)].data
        byte = len(data)
        push_modify_var_assign(data, byte, lvar)
        return

    # push new {$var1} {=} {'"문자열"'} {byte}
    m = re.match(r'push +new +\$([^ ]+) *= *([\'\"])(.*)\2 +(\d+)$', C.CMD)
    if m:
        var = m.group(1)
        byte = int(m.group(4))
        data = m.group(3)[:byte]
        
        push_new_var_assign(data, byte, var)
        return
    
    # push new {$var1} {=} {'"문자열"'}
    m = re.match(r'push +new +\$([^ ]+) *= *([\'\"])(.*)\2$', C.CMD)
    if m:
        var = m.group(1)
        data = m.group(3)
        byte = len(data)
        
        push_new_var_assign(data, byte, var)
        return
    
    # push new {$var1} {=} {$var2} {byte}
    m = re.match(r'push +new +\$([^ ]+) *= *([\'\"])(.*)\2 +(\d+)$', C.CMD)
    if m:
        var = m.group(1)
        byte = int(m.group(4))
        data = C.VARIABLES[m.group(3)].data[:byte]
        
        push_new_var_assign(data, byte, var)
        return
    
    # push new {$var1} {=} {$var2}
    m = re.match(r'push +new +\$([^ ]+) *= *([\'\"])(.*)\2$', C.CMD)
    if m:
        var = m.group(1)
        data = C.VARIABLES[m.group(3)].data
        byte = len(data)
        
        push_new_var_assign(data, byte, var)
        return
    
    # push {'"data"'} {byte}
    m = re.match(r'push +([\'\"])(.*)\1 +(\d+)$', C.CMD)
    if m:
        byte = m.group(3)
        data = m.group(2)[:byte]

        C.STACK.append(
            C.stack(data=data, assignedVar='', DLen=byte)
        )
        return

    # push {'"data"'}
    m = re.match(r'push +([\'\"])(.*)\1$', C.CMD)
    if m:
        data = m.group(2)
        byte = len(data)

        C.STACK.append(
            C.stack(data=data, assignedVar='', DLen=byte)
        )
        return
    
    # 지원하지 않는 문법 혹은 표현.
    ErrMsg('push')