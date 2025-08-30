from discord.ext import commands
from dotenv import load_dotenv
from discord import Message
import discord
import logging
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.event
async def on_message(message: Message):
    if message.author == bot.user: return

    print(f'Message from {message.author}')

    descriptions = []

    for attach in message.attachments:
        print("image" in attach.content_type, attach.filename)
        if "image" in attach.content_type:
            img_data = await attach.read()
            print(f'found image: {attach.filename}')

    await bot.process_commands(message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)