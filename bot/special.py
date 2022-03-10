import discord
from img.utils import arr_to_bytesIO

import tasks

import img

def run_code(message):
    """ Runs the code in a runner if possible
    
    Automatically answers accordingly
    """

    success, result, errmsg = tasks.run(message.content)

    if success:
        message.reply(file=discord.File(img.arr_to_bytesIO(result), filename="result.png"))
    else:
        message.reply(errmsg)
