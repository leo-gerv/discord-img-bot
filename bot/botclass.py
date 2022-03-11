# bot.py

from io import BytesIO
from PIL import Image
import discord
import logging
from .commands import image_treatments, special_commands
import re
import img as IMG

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

            if command in special_commands:
                success, result = special_commands[command](message, (await IMG.images_from_msg(message))[0])
                if success:
                    await message.reply(file=discord.File(result, filename="result.png"))
                else:
                    await message.reply(f"Failed to run your code: {result}")
                return

            img_handler = image_treatments[command]
            
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    img_bytes = await attachment.read()
                    img = Image.open(BytesIO(img_bytes))
                    result_img = img_handler(img.convert("RGB"))
                    with BytesIO() as f:
                        result_img.save(f, format="PNG")
                        f.seek(0)
                        fn_regex = r"(.*)\.[^.]*"
                        fn_match = re.match(fn_regex, attachment.filename)
                        fname = fn_match.group(1) + "_" + command + ".png"
                        await message.channel.send(file=discord.File(f, filename=fname))
            else:
                await message.reply("No image attached.")

        except Exception as e:
            await message.reply("Please specify a valid command.")
            logging.error(e)
