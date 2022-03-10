from .utils import prepare_dict

def run(text):
    """ Runs the code in the message
    
    Return value: (success, result)
        success: True if the code was found, False otherwise
        result: the result if success is True, None otherwise
    """

    ok, data = prepare_dict(text)
    if not ok:
        return (False, None)

    # TODO: Send the data to a runner

    return (True, None)
