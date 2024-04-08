import os
import random
import requests
from typing import Final
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents, Embed

# Cargar el token de discord
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# URL del archivo .txt en el repositorio de GitHub
github_file_url = 'https://raw.githubusercontent.com/matiasdante/cuackdae/main/patourl.txt?token=GHSAT0AAAAAACQVMDGBXF5VL5MZ32CXGUFMZQTNZ5Q'

# Descargar el archivo .txt desde el repositorio de GitHub
def download_image_list():
    response = requests.get(github_file_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f'Error al descargar el archivo: {response.status_code}')
        return []

# Descargar una imagen desde la URL
def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f'Error al descargar la imagen: {response.status_code}')
        return None

# Iniciar el bot
intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

# Cargar los nombres de archivos de imágenes desde el archivo .txt en GitHub
image_files = download_image_list()

# Comando para mostrar una imagen aleatoria
@client.command()
async def cr(ctx):
    if not image_files:
        await ctx.send('Error al cargar la lista de imágenes.')
        return
    
    # Seleccionar una imagen aleatoria de la lista
    random_image_url = random.choice(image_files)
    
    # Descargar la imagen desde la URL
    image_data = download_image(random_image_url)
    if image_data:
        # Crear un embed con la imagen adjunta
        embed = Embed(description=random_image_url, color=0xFFFF00)
        embed.set_image(url=random_image_url)
        
        # Enviar el embed con la imagen al chat
        await ctx.send(embed=embed)
    else:
        await ctx.send('Error al cargar la imagen.')

# Evento cuando el bot se conecta exitosamente
@client.event
async def on_ready():
    print(f'{client.user.name} está listo!')

# Conectar el bot con el token proporcionado
client.run(TOKEN)
