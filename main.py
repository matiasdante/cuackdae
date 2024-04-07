import os
import random

from typing import Final
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Context
from discord import Intents, Client, Message
from responses import get_response

# Cargar el token de discord

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')  # Token de discord.dev

# Iniciando bot

intents: Intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

# Cargar los nombres de archivos de imágenes desde el archivo "image_list.txt"
def load_image_list():
    with open('image_list.txt', 'r') as file:
        return file.read().splitlines()

# Primero Cuack

@client.command()
async def cr(ctx):
    # URL del repositorio de GitHub que contiene las imágenes
    github_repo_url = 'https://raw.githubusercontent.com/matiasdante/cuackdae_images/main/'

    # Cargar los nombres de archivos de imágenes desde "image_list.txt"
    image_files = load_image_list()

    # Seleccionar una imagen aleatoria de la lista
    random_image = random.choice(image_files)

    # Construir la URL completa de la imagen seleccionada
    image_url = github_repo_url + random_image

    # Enviar la imagen al chat
    await ctx.send(image_url)

# Evento cuando el bot se conecta exitosamente
@client.event
async def on_ready():
    print(f'¡{client.user.name} está listo!')

# Conectar el bot con el token proporcionado en el archivo "env"
client.run(TOKEN)