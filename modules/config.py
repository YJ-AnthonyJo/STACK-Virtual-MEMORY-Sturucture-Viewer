# config.py
STACK = list()
"""
STACK = [
    {'data' : str,
     'assignedVar': str,
     'RDistance(BP)': int,
     'dataLength' : int}
]
"""

VARIABLES = dict()
"""
# Case : Link with STACK 
- var 수정 -> stack도 수정.
- stack 수정 -> var수정.
```
STACK = [
    {'data' : $var['data'],
    'assignedVar' : 'var',
    'RDistance(BP) : int,
    'DLen' : $var['Dlen']}
]
```
```
VARIABLES = {
    'var' = {
        'type' : 'STACKLink',
        'data' : str,
        'DLen' : int
    }
}
```

# Case : Just var
```
VARIABLES = {
    'var' : {
        'type' : 'var',
        'data' : str,
        'Dlen' : int
    }
}
```

- VARIABLES의 type은 치역의 개념이다.
- stack의 assignedvar가 정의역개념이고.
- assignedvar -> type.
- 따라서 복수개의 STACK 데이터가 하나의 variable에 대입될 수 있다.

# Default Var
- int_max, int_min 등.. boundary값.

"""

commands = ["print", "push", "pop", "set", "clear", 'quit', 'delete']
CMD = ''

EnvVar = {
    "MultiLineP" : "Yes", # 문자열. 'Yes' or 'No'
    "regType" : 32, # 정수. 32 or 64
    "Base" : "BP"
}