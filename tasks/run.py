from .utils import prepare_dict
from .pool import assign_handle

def run(text):
    """ Runs the code in the message
    
    Return value: (success, result)
        success: True if the code was found, False otherwise
        result: the result if success is True, None otherwise
        errmsg: the error message if success is False, None otherwise
    """

    ok, data = prepare_dict(text)
    if not ok:
        return (False, None, 'Invalid code tags')

    # TODO: Send the data to a runner
    ok, handle = assign_handle()

    if not ok:
        return (False, None, 'No runners available')

    ok, result, errmsg = handle.process(data)

    if not ok:
        return (False, None, errmsg)

    return (True, result, None)
