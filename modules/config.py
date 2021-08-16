#config.py
STACK = list() # [ ['{vari}', '{data}', {byte}], ...]
"""
STACK = [
    {'data' : str,
     'assignedVar': str,
     'RDistance(BP)': int,
     'dataLength' : int}
]
"""

VARIABLES = dict()
idx_of_vari_tmp = 0
commands = ["print", "push", "pop", "set", "clear", 'quit']
CMD = ''