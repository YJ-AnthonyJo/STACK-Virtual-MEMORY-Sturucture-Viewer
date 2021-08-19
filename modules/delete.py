from modules.config import STACK
from Func import *
import config as C
import re

def init():
    m_v = re.match(r'delete +\$([^ ]+)', C.CMD)
    m_s = re.match(r'delete +(.*)([-+] *\d+)$', C.CMD)
    if m_v or m_s: # delete $var
        if m_v:
            var = m_v.group(1)
            if not chk_var_in_VARIABLES(True, var) : return
            print(f'${var}', '=', C.VARIABLES[var])
            
            if input(f'Really Delete ${var}?(Y/N)').lower().startswith('y'):
                C.VARIABLES.pop(var) # ISSUE 34번을 위해 del()대신 pop사용.
        elif m_s:
            base = m_s.group(1)
            base = base.rstrip() if base != '' else 'ebp'
            Rlength = int(m_s.group(2).replace(' ', ''))
            if base.lower() in ['esp', 'rsp']:
                idx = next((i for i, data in enumerate([sum([d["DLength"] for d in C.STACK[idx + 1:]]) for idx in range(len(C.STACK))]) if data == Rlength), None)
                quest = f'{"E" if C.EnvVar["regType"] == 32 else "R"}SP+{Rlength} which is \'{C.STACK[idx]["data"]}\''

            elif base.lower() in ['ebp', 'rbp']:
                idx = next( (index for (index, d) in enumerate(C.STACK) if d["RDistance(BP)"] == Rlength), None)
                quest = f'{"E" if C.EnvVar["regType"] == 32 else "R"}BP{format(Rlength,"+d")} which is \'{C.STACK[idx]["data"]}\''
            
            if idx != None:
                if input(f'Really Delete {quest}? ').lower().startswith('y'):
                    del C.STACK[idx]
                    reset_RDistance_BP()
                    print(f'Deleted {quest}')
                    
            else:
                print("Relative address is invalid.")