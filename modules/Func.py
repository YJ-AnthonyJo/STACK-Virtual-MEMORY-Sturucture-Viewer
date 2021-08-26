'''
Contains Useful Function.
**LIST**
1. chk_valid_variable_name(*vars)
        check if string input as vairable name is correct to use according to python variable convention.

'''
import re, json
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
        else: return byte # 원래 : -byte

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
        m = re.match(r'(.+) +(\d+)$', var)
        if m:
            var = m.group(1)
            byte = int(m.group(2))
            return True, var, byte
        else:
                m = re.match(r'([^ ]+)$', var)
                if m:
                        if not chk_var_in_VARIABLES(True, var) : return [False] * 2
                        byte = C.VARIABLES[var]['DLen']
                        return True, var, byte
        return [False] * 3
        

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
        '''
        LWS여부 판단 후 알맞은 데이터, 변수(assignedVar에 들어갈)이름 반환.
        
        :parm byte : var에서 시용할 바이트 크기
        :parm var : 변수 이름
        
        :return data, assignedVar : STACK에 들어갈 데이터
        '''
        if byte >= C.VARIABLES[var].DLen:
                # LWS 처리.
                data = ''
                var = var
                C.VARIABLES[var].type = 'STACKLink'
                return data, var
        else:
                data = C.VARIABLES[var].data[:byte]
                var = ''
                return data, var

def init_set_STACK(m):
        #기준 정하기. esp? ebp?
        base = m.group(1)
        base = base.rstrip() if base != '' else 'ebp'
        #상대주소 +num, -num
        relativeAddr = int(m.group(2).replace(' ', '')) 
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
                _, r_var, byte = set_var_and_byte(r_var)
                if not _ or not chk_var_in_VARIABLES(True, r_var) : return [False] * 3
                data = C.VARIABLES[r_var]['data'][:byte]
                return True, data, byte
        else:
                return [False] * 3

def case_set_var_2(r_value):
        m = re.match(r'([\'\"])(.*)\1 *(\d*)$', r_value)
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
            var = m.group(1).rstrip()
            _, var, byte = set_var_and_byte(var)
            if not _ or not chk_var_in_VARIABLES(True, var): return [False] * 4
            
            data, var = LWS(byte, var)
            return True, data, var, byte
        else:
                return [False] * 4

def case_set_STACK_2(r_value):
        m = re.match(r'([\'\"])(.*)\1 *(\d*)$', r_value)
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

def adjust_set_STACK(new, base, *args):
        if base.lower() in ['esp', 'rsp']:
                idx = next((i for i, data in enumerate([sum([d["DLength"] for d in C.STACK[idx + 1:]]) for idx in range(len(C.STACK))]) if data == args[-2]), None)
        elif base.lower() in ['ebp', 'rbp']:
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


def print_stack_v1(data, maxDataLen, PrintData, idx):
        '''.....으로 대체'''
        LineNum = data['DLength'] // (C.EnvVar['regType'] // 8) + int(data['DLength'] % (C.EnvVar['regType'] // 8) != 0) #현 데이터당 출력 줄수 지정. data가 4바이트일 때까지 한 줄에 표시. data가 5바이트면 2줄.
        
        for _ in range(1, LineNum): print("|", ' ' * maxDataLen, '|') # 마지막 줄 전까지 공백 출력.
        PData = PrintData(data)
        
        # 작업.
        if len(PData) > maxDataLen:
            PData = PData[:maxDataLen-5] + '.....'
            pass
        
        print('|', PData, ' '*(maxDataLen-len(PData)), end='') # 마지막 줄에 데이터 출력.
        
        if C.EnvVar['Base'] == 'BP':
                sign = 1 if data["RDistance(BP)"] >= 0 else 0 #양수여부.
                if data['RDistance(BP)'] == 0: print('| <= {}BP'.format('E' if C.EnvVar['regType'] == 32 else 'R'))
                else: print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}BP {"+" if sign else "-"} {str(data["RDistance(BP)"])[0 if sign else 1:]}') #| <= EBP - N //OR// | <= EBP + N
        else:
                if idx == len(C.STACK) - 1 : print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}SP')
                else : print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}SP + {sum([d["DLength"] for d in C.STACK[idx + 1:]])}') #| <= EBP - N //OR// | <= EBP + N
        
        print('-' * (maxDataLen + 4))

def print_stack_v2(data, maxDataLen, PrintData, idx):
        '''복수줄에 표시.(4바이트 넘을 시.)'''
        LineNum = data['DLength'] // (C.EnvVar['regType'] // 8) + int(data['DLength'] % (C.EnvVar['regType'] // 8) != 0) #현 데이터당 출력 줄수 지정. data가 4바이트일 때까지 한 줄에 표시. data가 5바이트면 2줄.
        
        PData = [PrintData(data)]
        if len(PData[0]) > maxDataLen and LineNum >= 2:
                tmp = len(PData[0]) // maxDataLen + int(len(PData[0]) % maxDataLen != 0)
                _ = tmp # 예외처리를 위한 백업.
                tmp = tmp if tmp <= LineNum else LineNum
                PData = [PData[0][st:st+maxDataLen] for st in [i * maxDataLen for i in range(tmp)]]
                if _ > LineNum: # 출력가능 줄 수보다 데이터가 많은 경우.. 테스트 할 케이스나 실제 사용될 경우가 없을 듯하다.
                        PData[-1] = PData[-1][:maxDataLen-5] + '.....'
                
                
        for _ in range(1, LineNum - len(PData) + 1): print("|", ' ' * maxDataLen, '|') # 마지막 줄 전까지 공백 출력.
        
        for _ in PData[:-1]: print('|', _, ' '*(maxDataLen-len(_)), end='|\n') # 데이터 출력.
        print('|', PData[-1], ' '*(maxDataLen-len(PData[-1])), end='') # 마지막 줄, 데이터 출력.
        
        
        if C.EnvVar['Base'] == 'BP':
                sign = 1 if data["RDistance(BP)"] >= 0 else 0 #양수여부.
                if data['RDistance(BP)'] == 0: print('| <= {}BP'.format('E' if C.EnvVar['regType'] == 32 else 'R'))
                else: print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}BP {"+" if sign else "-"} {str(data["RDistance(BP)"])[0 if sign else 1:]}') #| <= EBP - N //OR// | <= EBP + N
        else:
                if idx == len(C.STACK) - 1 : print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}SP')
                else : print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}SP + {sum([d["DLength"] for d in C.STACK[idx + 1:]])}') #| <= EBP - N //OR// | <= EBP + N
        
        print('-' * (maxDataLen + 4))

def EnvVarInit():
        try:
                f = open('./modules/EnvVars.json')
                s = f.read()
                f.close()
                
                _ = json.loads(s)
                C.EnvVar = _
        except:
                print('Error on Reading Envvars.json\nSet to Default.')