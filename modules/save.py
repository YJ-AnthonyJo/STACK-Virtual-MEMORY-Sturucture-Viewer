from modules.Func import ErrMsg
import re
import config as C
import json, inspect

def init():
    m = re.match(r'save +([\'\"])([^\/:*?"<>|]+)\1$', C.CMD)
    m1 = re.match(r'save$', C.CMD)
    if m or m1:
        with open(m.group(2) if m else 'STACK_VIEWER.json', 'w') as f:
            f.write(
                inspect.cleandoc(
                    f'''
                    {{
                        "STACK" : {json.dumps(C.STACK)},
                        "VARIABLES" : {json.dumps(C.VARIABLES)}
                    }}
                    '''
                )
            )
    else:
        ErrMsg('save')