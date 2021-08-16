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
        'Dlen' : int
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

# Default Var
- int_max, int_min 등.. boundary값.

"""

commands = ["print", "push", "pop", "set", "clear", 'quit']
CMD = ''