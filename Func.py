import re
import inspect
def chk_valid_variable_name(*varis):
    '''
    USEAGE
    if not chk_valid_variable_name(vari1, vari2):
            return
    '''
    for vari in varis:
        p = re.compile("^[a-zA-Z_$ㄱ-ㅎ가-힣ㅏ-ㅣ][\wㄱ-ㅎ가-힣ㅏ-ㅣ$]*$")
        if not bool(p.match(vari)):
            print(inspect.cleandoc("""Syntax Error! : Invalid Variable name
                    Check valid Variable name by help(varialbe_name)
                    if you evaluate your expression are rigth, please add issue AT 
                       https://github.com/YJ-AnthonyJo/STACK-Virtual-MEMORY-Sturucture-Viewer/issues/"""))
            return False
    return True