import os
import random
import requests

from typing import Final
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Context
from discord import Intents, Client, Message

# Cargar el token de discord
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')  # Token de discord.dev

# URL del archivo .txt en el repositorio de GitHub
github_file_url = 'https://raw.githubusercontent.com/matiasdante/cuackdae/main/patourl.txt?token=GHSAT0AAAAAACQTF37NH3GGKWT6AMZFFQFEZQSJYYA'

# Descargar el archivo .txt desde el repositorio de GitHub
def download_image_list():
    response = requests.get(github_file_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f'Error al descargar el archivo: {response.status_code}')
        return []

# Iniciando bot
intents: Intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

# Cargar los nombres de archivos de imágenes desde el archivo .txt en GitHub
image_files = download_image_list()

# Primero Cuack
@client.command()
async def cr(ctx):
    if not image_files:
        await ctx.send('Error al cargar la lista de imágenes.')
        return

    # Seleccionar una imagen aleatoria de la lista
    random_image = random.choice(image_files)

    # Enviar la imagen al chat
    await ctx.send(random_image)

# Evento cuando el bot se conecta exitosamente
@client.event
async def on_ready():
    print(f'¡{client.user.name} está listo!')

# Conectar el bot con el token proporcionado en el archivo "env"
client.run(TOKEN)
