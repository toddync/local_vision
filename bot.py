import os

from discord.ext import commands
from dotenv import load_dotenv
from discord import Message
import discord
import httpx
import base64

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
        if "image" in attach.content_type:
            img_data = await attach.read()
            print(f'found image: {attach.filename}')
            description = await get_image_description(img_data)
            await message.reply(f"I see an image: {description}")

    await bot.process_commands(message)

async def get_image_description(image_data: bytes) -> str:
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llava-phi3",
        "prompt": "Analyze this image in detail. First, identify the main subject and the overall setting. Then, list the key objects and their spatial relationships. Finally, describe the mood and any notable actions.",
        "images": [encoded_image],
        "stream": False,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("https://d38d14803ae0.ngrok-free.app/api/generate", headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            response_data = response.json()
            print(response_data["response"])
            description = response_data["response"]
            return description
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
            return "Could not get a description for the image."
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url!r}: {e}")
            return "Could not get a description for the image."
        except KeyError:
            print("Unexpected response format from Ollama.")
            return "Could not get a description for the image due to unexpected response format."