# bot.py

import discord
import logging

class Bot(discord.Client):
    """ Discord bot class

        Interacts with discord.py to listen for events and handle them accordingly.
    """

    async def on_ready(self):
        """ On ready event handler.

            When the bot is ready, print a message to the console.
        """
        logging.info("Bot is ready.")

    async def on_message(self, message):
        """ On message event handler.

            Only read message mentioning the bot.
        """
        logging.info("Message received.")
        if message.author == self.user:
            return

        first_mention = message.mentions[0] if len(message.mentions) > 0 else None

        if first_mention and first_mention.id == self.user.id:
            await message.channel.send("Hello!")
