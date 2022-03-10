'''
    Discord multi-purpose image bot

    main.py
    Entry point for the bot.
'''

import os
import bot

if __name__ == '__main__':
    bot = bot.Bot(os.environ['TOKEN'])
