import json, re
from modules.Func import ErrMsg
import config as C

def init():
    if not (len(C.STACK) == 0 and len(C.VARIABLES) == 0) : return print('ERROR : STACK and VARIABLES must be empty to load.')
    m = re.match(r'load +([\'\"])([^\/:*?"<>|]+)\1$', C.CMD)
    m1 = re.match(r'load$', C.CMD)
    if m or m1:
        with open(m.group(2) if m else 'STACK_VIEWER.json', 'r') as f:
            try:
                LodaedData = json.load(f)
            except:
                print('ERR : Fail to load file as json expression')
                f.close()
                return
        C.STACK = LodaedData['STACK']
        C.VARIABLES = LodaedData['VARIABLES']
    else:
        ErrMsg('load')