'''
    Discord multi-purpose image bot

    main.py
    Entry point for the bot.
'''

import asyncio
import logging
import os
from time import sleep
import bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET)
    bot = bot.Bot(os.environ['TOKEN'])
    asyncio.run(bot.run())
