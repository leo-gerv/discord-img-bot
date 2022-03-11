def generate_code_str(body, argname, global_name):
    """ Generate python code to eval()
    """
    body = body.replace('\n', '\n    ')
    
    return f"""def f({argname}):
    {body}

output = f({global_name})"""
