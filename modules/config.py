#config.py
STACK = list() # [ ['{vari}', '{data}', {byte}], ...]
"""
STACK = [
    {'assignedVar': str,
     'RelativeDistance(base: EBP, RBP)': int,
     'RelativeDistance(base: ESP, RSP)': int,
     'dataLength' : int}
]
"""

VARIABLES = dict()
idx_of_vari_tmp = 0
commands = ["print", "push", "pop", "set", "clear", 'quit']
CMD = ''