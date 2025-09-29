import os

from discord.ext import commands
from dotenv import load_dotenv
from discord import Message
import discord
import httpx
import base64

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
url = os.getenv("API_URL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logado como {bot.user.name}")
    print("------")


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    print(f"Mensagem de {message.author}")

    for attach in message.attachments:
        if "image" in attach.content_type:
            img_data = await attach.read()
            print(f"imagem encontrada: {attach.filename}")
            description = await get_image_description(img_data)
            await message.reply(f"Eu vejo uma imagem: {description}")

    await bot.process_commands(message)


async def get_image_description(image_data: bytes) -> str:
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llava-phi3",
        "prompt": "Analise esta imagem em detalhes. Primeiro, identifique o assunto principal e o cenário geral. Em seguida, liste os objetos chave e suas relações espaciais. Finalmente, descreva o humor e quaisquer ações notáveis.",
        "images": [encoded_image],
        "stream": False,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://d38d14803ae0.ngrok-free.app/api/generate",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()
            response_data = response.json()
            print(response_data["response"])
            description = response_data["response"]
            return description
        except httpx.RequestError as e:
            print(f"Ocorreu um erro ao solicitar {e.request.url!r}: {e}")
            return "Não foi possível obter uma descrição para a imagem."
        except httpx.HTTPStatusError as e:
            print(
                f"Resposta de erro {e.response.status_code} ao solicitar {e.request.url!r}: {e}"
            )
            return "Não foi possível obter uma descrição para a imagem."
        except KeyError:
            print("Formato de resposta inesperado do Ollama.")
            return "Não foi possível obter uma descrição para a imagem devido ao formato de resposta inesperado."
