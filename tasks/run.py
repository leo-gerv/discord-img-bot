from .utils import prepare_dict
from .pool import assign_handle

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
    ok, handle = assign_handle()

    if not ok:
        return (False, None)

    ok, result = handle.process(data)

    if not ok:
        return (False, None)

    return (True, result)
