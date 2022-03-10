import numpy as np

def generate_code_str(body, argname, global_name):
    """ Generate python code to eval()
    """
    
    return f"""def f({argname}):
    {body}

f({global_name})"""
