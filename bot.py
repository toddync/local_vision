import os

from discord.ext import commands
from dotenv import load_dotenv
from discord import Message
import discord

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    print(f'Message from {message.author}')

    for attach in message.attachments:
        print("image" in attach.content_type, attach.filename)
        if "image" in attach.content_type:
            img_data = await attach.read()
            print(f'found image: {attach.filename}')

    await bot.process_commands(message)