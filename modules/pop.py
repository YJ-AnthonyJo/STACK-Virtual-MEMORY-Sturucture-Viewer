import config as C
import re
def pop():
    if len(C.STACK) == 0:
            print("Empty STACK")
            return False
        
    C.CMD = C.CMD.split()
    if len(C.CMD) == 1: #parm이 주어지지 않았을 때, 즉 pop만하고 버릴 때.
        C.STACK.pop()
    else: #parm이 주어졌을 때.
        #아래 두 if => 변수명으로 사용 불가능한 것 필터링.
        if C.CMD[1] == 'all': #all필터링.
            print(f"You can't use all as variable name, temporary stored in tmp_{C.idx_of_vari_tmp}")
            C.VARIABLES[f'tmp_{C.idx_of_vari_tmp}'] = C.STACK.pop()
            print(f'tmp_{C.idx_of_vari_tmp} =', C.VARIABLES[f"tmp_{C.idx_of_vari_tmp}"])
            C.idx_of_vari_tmp += 1
            return False
        if re.match('\d*:\d*$', C.CMD[1]): #{:}, {숫자:숫자} 필터링.
            print(f"You can't use : in variable name temporary stored in tmp_{C.idx_of_vari_tmp}")
            C.VARIABLES[f'tmp_{C.idx_of_vari_tmp}'] = C.STACK.pop()
            print(f'tmp_{C.idx_of_vari_tmp} =', C.VARIABLES[f"tmp_{C.idx_of_vari_tmp}"])
            C.idx_of_vari_tmp += 1
            return False
        #필터링 통과했을 때, VARIABLES에 pop된 값 저장.
        C.VARIABLES[C.CMD[1]] = C.STACK.pop()
        print(C.CMD[1], '=', C.VARIABLES[C.CMD[1]])
        return False #아래 if문 통과.