import config as C
from Func import *

def push_modify_var_assign(data, byte, var) -> (None):
    idx = C.STACK.indexA('assignedVar', var)
    for i in idx:
        C.STACK[i].DLen = byte
    if idx != [] : reset_RDistance_BP()
    
    C.VARIABLES[var] = C.var(data=data[:byte], DLen =byte,type_='STACKLink')
    
    C.STACK.append(
        C.stack(data='', assignedVar=var, DLen=byte)
    )

def push_new_var_assign(data, byte, var) -> (None):
    C.VARIABLES.new(
        var, 
        C.var(data=data[:byte], DLen=byte, type_='STACKLink')
    )
    C.STACK.append(
        C.stack(data='', assignedVar=var, DLen=byte)
    )