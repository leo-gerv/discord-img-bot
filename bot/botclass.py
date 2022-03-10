# bot.py

from io import BytesIO
import discord
import logging
from .commands import image_treatments

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
            await self.handle_request(message)
            

    async def handle_request(self, message):
        """ Handle a request
        """
        try:
            command = message.content.split(" ")[1]

            img_handler = image_treatments[command]
            
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    img_bytes = await attachment.read()
                    img_bytes = img_handler(img_bytes)
                    await message.reply(file=discord.File(BytesIO(img_bytes), filename=attachment.filename))
            else:
                await message.reply("No image attached.")

        except Exception as e:
            await message.reply("Please specify a valid command.")
            logging.error(e)
