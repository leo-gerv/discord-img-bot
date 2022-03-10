# bot.py

import discord
import logging

class Bot:
    """ Discord bot class

        Interacts with discord.py to listen for events and handle them accordingly.
    """

    def __init__(self, token):
        """ Initialize the bot.

            Args:
                token (str): Discord bot token.
        """
        self.token = token
        self.client = discord.Client()

        # event handlers
        self.client.on_ready = self.on_ready

    async def on_ready(self):
        """ On ready event handler.

            When the bot is ready, print a message to the console.
        """
        logging.info("Bot is ready.")
