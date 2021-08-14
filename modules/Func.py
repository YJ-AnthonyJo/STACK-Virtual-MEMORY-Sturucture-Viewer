'''
Contains Useful Function.
**LIST**
1. chk_valid_variable_name(*vars)
        check if string input as vairable name is correct to use according to python variable convention.

'''
import re
import inspect


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