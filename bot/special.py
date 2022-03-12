import discord
from img.utils import arr_to_bytesIO

import tasks
import numpy as np

import img

async def run_code(message, in_img):
    """ Runs the code in a runner if possible
    
    Returns a tuple (success, result)
    """

    success, result, errmsg = await tasks.run(message.content, np.array(in_img))

    if success:
        return True, img.arr_to_bytesIO(result)
    else:
        return False, errmsg
