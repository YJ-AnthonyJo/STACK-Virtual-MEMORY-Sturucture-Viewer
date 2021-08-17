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
            byte = C.VARIABLES[var]['DLen']
        return var, byte

def ErrMsg(func):
        print(inspect.cleandoc(f"""Syntax Error. Please Check Manual Using help({func})
                If Something Wrong with syntax, etc.. Please add Issue at
                https://github.com/YJ-AnthonyJo/STACK-Virtual-MEMORY-Sturucture-Viewer/issues/"""))

def chk_var_in_VARIABLES(want, var): #want : 바람(원하는 것)
        if var in C.VARIABLES:
                if want == False: #있지만 하지만 없는 것을 바람
                        print("This Variable name is already exist, please use other.")
                        return False
                else: #있고, 있기를 바람
                        return True
        else:
                if want == True: #없지만 있는 것을 바람
                        print(f"{var} is not assigned. please check variables using print all")
                        return False
                else: #없고, 없기를 바람
                        return True

def LWS(byte, var):
        if byte >= C.VARIABLES[var]['DLen']:
                # LWS 처리.
                data = ''
                var = var
                C.VARIABLES[var]['type'] = 'STACKLink'
                return data, var
        else:
                data = C.VARIABLES[var]['data'][:byte]
                var = ''
                return data, var

def init_set_STACK(m):
        #기준 정하기. esp? ebp?
        base = m.group(1)
        base = base if base != '' else 'ebp'
        #상대주소 +num, -num
        relativeAddr = int(m.group(2)) 
        r_value = m.group(3)
        return base, relativeAddr, r_value

def init_set_var(m):
        l_var = m.group(1).rstrip()
        r_value = m.group(2)
        return l_var, r_value

def case_set_var_1(r_value):
        m = re.match(r'\$(.+)', r_value)
        if m:
                r_var = m.group(1).rstrip()
                r_var, byte = set_var_and_byte(r_var)
                if not chk_valid_variable_name(r_var) : return [False] * 3
                data = C.VARIABLES[r_var]['data'][:byte]
                return True, data, byte
        else:
                return [False] * 3

def case_set_var_2(r_value):
        m = re.match(r'([\'\"])(.*)\1 *(\d*)', r_value)
        if m:
                data = m.group(2)
                byte = m.group(3)
                byte = int(byte) if byte != '' else len(data)
                data = data[:byte]
                return True, data, byte
        else:
                return [False] * 3

def case_set_STACK_1(r_value):
        m = re.match(r'\$(.+)', r_value) 
        if m:
            #변수명 받기.
            var = m.group(1)
            var, byte = set_var_and_byte(var)
            if not chk_var_in_VARIABLES(True, var): return [False] * 4
            
            data, var = LWS(byte, var)
            return True, data, var, byte
        else:
                return [False] * 4

def case_set_STACK_2(r_value):
        m = re.match(r'([\'\"])(.*)\1 *(\d*)', r_value)
        if m:
                #데이터 입력받기.
                data = m.group(2)

                #byte받기.    
                byte = m.group(3)
                byte = int(byte) if byte != '' else len(data)

                data = data[:byte]
                var = ''
                return True, data, var, byte
        else:
                return [False] * 4

def adjust_set_STACK(new, *args):
        idx = next( (index for (index, d) in enumerate(C.STACK) if d["RDistance(BP)"] == args[-2]), None)
        if idx != None:
                _exec = inspect.cleandoc("""
                C.STACK{0}{{
                'data' : {2!r},
                'assignedVar' : {3!r},
                'RDistance(BP)' : {4!r},
                'DLength' : {5!r}
                }}{1}
                reset_RDistance_BP()
                """.format('.insert(idx, ' if new == True else '[idx] = ', ')' if new == True else '', *args))
                exec(_exec)
        else:
                print("relative address is invalid.") # ISSUE #21


def modify_VARIABLE_chk_STACK(var, byte):
        # 기존에 존재하는 변수가 바뀌었는데 그 변수의 type이 LWS였을 때,
        # 해당 변수을 사용하는 STACK을 수정해준다.
        idx = list(
                filter(
                        lambda x: C.STACK[x]['assignedVar'] == var, range(len(C.STACK))
                        )
                )
        for i in idx:
                C.STACK[i]['DLength'] = byte
        if idx != [] : reset_RDistance_BP()