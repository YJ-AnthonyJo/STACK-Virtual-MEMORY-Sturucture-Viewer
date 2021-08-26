import config as C

def get_max(lmb):
        M = lmb(C.STACK[0])
        for d in C.STACK[1:]:
                _ = lmb(d)
                if M < _: M = _
        return M

def print_stack_v1(data, maxDataLen, PrintData, idx):
        '''.....으로 대체'''
        LineNum = data['DLen'] // (C.EnvVar['regType'] // 8) + int(data['DLen'] % (C.EnvVar['regType'] // 8) != 0) #현 데이터당 출력 줄수 지정. data가 4바이트일 때까지 한 줄에 표시. data가 5바이트면 2줄.
        
        for _ in range(1, LineNum): print("|", ' ' * maxDataLen, '|') # 마지막 줄 전까지 공백 출력.
        PData = PrintData(data)
        
        # 작업.
        if len(PData) > maxDataLen:
            PData = PData[:maxDataLen-5] + '.....'
            pass
        
        print('|', PData, ' '*(maxDataLen-len(PData)), end='') # 마지막 줄에 데이터 출력.
        
        if C.EnvVar['Base'] == 'BP':
                sign = 1 if data["RDistance_BP"] >= 0 else 0 #양수여부.
                if data['RDistance_BP'] == 0: print('| <= {}BP'.format('E' if C.EnvVar['regType'] == 32 else 'R'))
                else: print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}BP {"+" if sign else "-"} {str(data["RDistance_BP"])[0 if sign else 1:]}') #| <= EBP - N //OR// | <= EBP + N
        else:
                if idx == len(C.STACK) - 1 : print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}SP')
                else : print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}SP + {sum([d["DLength"] for d in C.STACK[idx + 1:]])}') #| <= EBP - N //OR// | <= EBP + N
        
        print('-' * (maxDataLen + 4))

def print_stack_v2(data, maxDataLen, PrintData, idx):
        '''복수줄에 표시.(4바이트 넘을 시.)'''
        LineNum = data['DLen'] // (C.EnvVar['regType'] // 8) + int(data['DLen'] % (C.EnvVar['regType'] // 8) != 0) #현 데이터당 출력 줄수 지정. data가 4바이트일 때까지 한 줄에 표시. data가 5바이트면 2줄.
        
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
                sign = 1 if data["RDistance_BP"] >= 0 else 0 #양수여부.
                if data['RDistance_BP'] == 0: print('| <= {}BP'.format('E' if C.EnvVar['regType'] == 32 else 'R'))
                else: print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}BP {"+" if sign else "-"} {str(data["RDistance_BP"])[0 if sign else 1:]}') #| <= EBP - N //OR// | <= EBP + N
        else:
                if idx == len(C.STACK) - 1 : print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}SP')
                else : print(f'| <= {"E" if C.EnvVar["regType"] == 32 else "R"}SP + {sum([d["DLen"] for d in C.STACK[idx + 1:]])}') #| <= EBP - N //OR// | <= EBP + N
        
        print('-' * (maxDataLen + 4))