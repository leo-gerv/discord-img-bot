import re

def extract_code(text):
    """ Extracts the python code from the message

    Return value: (success, code)
        success: True if the code was found, False otherwise
        code: the code if success is True, None otherwise
    """

    regex = r"(?s)```(python)?(\n)?(.*?)```"
    match = re.search(regex, text)
    if match:
        return (True, match.group(3))
    else:
        return (False, None)

def prepare_dict(text):
    """ Prepares the dictionary to be sent to the runner

    Return value: (success, dict)
        success: True if the code was found, False otherwise
        dict: the dictionary if success is True, None otherwise
    """

    ok, code = extract_code(text)

    if not ok:
        return (False, None)

    return (True, {'body': code, 'argname': 'array', 'global_name': 'in_array'})
