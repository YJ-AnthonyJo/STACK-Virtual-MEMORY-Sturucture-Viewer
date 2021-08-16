'''
Contains Useful Function.
**LIST**
1. chk_valid_variable_name(*vars)
        check if string input as vairable name is correct to use according to python variable convention.

'''
import enum
import re
import inspect
import config as C

def chk_valid_variable_name(*vars):
    '''
    USEAGE
    if not chk_valid_variable_name(*vars):
            return
    '''
    for var in vars:
        p = re.compile("^[a-zA-Z_$ㄱ-ㅎ가-힣ㅏ-ㅣ][\wㄱ-ㅎ가-힣ㅏ-ㅣ$]*$")
        if not bool(p.match(var)):
            print(inspect.cleandoc("""Syntax Error! : Invalid Variable name
                    Check valid Variable name by help(varialbe_name)
                    if you evaluate your expression are rigth, please add issue AT 
                       https://github.com/YJ-AnthonyJo/STACK-Virtual-MEMORY-Sturucture-Viewer/issues/"""))
            return False
    return True

def Calc_RDistance( byte ):        
        if len(C.STACK) != 0: 
                sign = 1 if C.STACK[-1]['RDistance(BP)'] >= 0 else 0
                if sign:
                        return C.STACK[-1]['RDistance(BP)'] + byte
                else:
                        return C.STACK[-1]['RDistance(BP)'] - byte
        else: return -byte

def reset_RDistance_BP():
        """STACK = [
        {'assignedVar': str,
        'RDistance(BP)': int,
        'DLength' : int}
        ]"""
        Len = len(C.STACK)
        if Len == 0 : return
        
        BPIdx = next( (index for (index, d) in enumerate(list(reversed(C.STACK))) if d["data"] in ['sfp', 'Sfp', 'sFp', 'sfP', 'SFp', 'SfP', 'SFP']), None)
        if BPIdx != None:
                BPIdx = Len - 1 - BPIdx
                C.STACK[BPIdx]['RDistance(BP)'] = 0
                for rev_idx in range(BPIdx - 1, -1, -1):
                        C.STACK[rev_idx]['RDistance(BP)'] = \
                                C.STACK[rev_idx + 1]['RDistance(BP)'] + C.STACK[rev_idx + 1]['DLength']
                for idx in range(BPIdx + 1, Len):
                        C.STACK[idx]['RDistance(BP)'] = \
                                C.STACK[idx - 1]['RDistance(BP)'] - C.STACK[idx]['DLength']
        else:
                C.STACK[0]['RDistance(BP)'] = - C.STACK[0]['DLength']
                for idx in range(1, Len):
                        C.STACK[idx]['RDistance(BP)'] = \
                                C.STACK[idx - 1]['RDistance(BP)'] - C.STACK[idx]['DLength']

chk_sfp = lambda data : reset_RDistance_BP() if data in ['sfp', 'Sfp', 'sFp', 'sfP', 'SFp', 'SfP', 'SFP'] else None


def get_max(lamb):
        M = lamb(C.STACK[0])
        for d in C.STACK[1:]:
                _ = lamb(d)
                if M < _: M = _
        return M

def set_var_and_byte(var):
        m = re.match(r'(.+) +(\d+)', var)
        if m:
            var = m.group(1)
            byte = int(m.group(2))
        else:
            byte = len(C.VARIABLES[var])
        return var, byte

def ErrMsg(func):
        print(inspect.cleandoc(f"""Syntax Error. Please Check Manual Using help({func})
                If Something Wrong with syntax, etc.. Please add Issue at
                https://github.com/YJ-AnthonyJo/STACK-Virtual-MEMORY-Sturucture-Viewer/issues/"""))

def chk_var_in_VARIABLES(var):
        if var in C.VARIABLES:
            print("This Variable name is already exist, please use other.")
            return