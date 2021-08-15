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
def Calc_RDistance( byte, base ):        
        
        if len(C.STACK) != 0:
                return C.STACK[-1][base] + byte
        else:
                
                
                # if BPIdx > 
                return byte
def reset_RDistance_BP():
        #for (idx, data) in enumerate(C.STACK):
        #for rev_idx in range(len(C.STACK), -1, -1):
        """STACK = [
        {'assignedVar': str,
        'RDistance(BP)': int,
        'RDistance(SP)': int,
        'DLength' : int}
        ]
        """
        Len = len(C.STACK)
        BPIdx = next( (index for (index, d) in enumerate(list(reversed(C.STACK))) if d["data"] in ['Sfp', 'sFp', 'sfP', 'SFp', 'SfP', 'SFP']), None)
        BPIdx -= Len
        C.STACK[BPIdx]['RDistance(BP)'] = 0
        for rev_idx in range(BPIdx - 1, -1, -1):
                C.STACK[rev_idx]['RDistance(BP)'] = \
                        C.STACK[rev_idx + 1]['RDistance(BP)'] + C.STACK[rev_idx]['byte']
        for idx in range(BPIdx, Len + 1):
                C.STACK[idx]['RDistance(BP)'] = \
                        C.STACK[idx - 1]['RDistance(BP)'] + C.STACK[idx]['byte']