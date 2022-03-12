import logging
from .utils import prepare_dict
import numpy as np
from .pool import get_handle

async def run(text, array):
    """ Runs the code in the message
    
    Return value: (success, result)
        success: True if the code was found, False otherwise
        result: the result if success is True, None otherwise
        errmsg: the error message if success is False, None otherwise
    """

    ok, data = prepare_dict(text)
    if not ok:
        return (False, None, 'Invalid code tags')

    handle = get_handle()

    if not handle:
        return (False, None, 'No runners available')

    data['array'] = array
    ok, result, errmsg = await handle.process(data)

    if not ok:
        return (False, None, errmsg)

    return (True, np.array(result), None)
