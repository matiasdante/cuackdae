import os
import random
import requests
from typing import Final
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents, Embed, Activity, ActivityType
import discord
import mysql.connector
from datetime import datetime, timedelta

# Cargar el token de discord
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Configuración de la base de datos
db_config = {
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'host': 'localhost',
    'database': 'tu_basedatos'
}

# Crear la conexión
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# URL del archivo .txt en el repositorio de GitHub
github_file_url = 'https://raw.githubusercontent.com/matiasdante/cuackdae/main/patourl.txt'

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

# Obtener el título de la imagen desde la URL
def get_image_title(url):
    # Obtener la parte de la URL que contiene el nombre de la imagen
    image_name = url.split('/')[-1]
    
    # Eliminar la extensión (.jpg, .png, etc.)
    image_title = image_name.split('.')[0]
    
    # Reemplazar guiones medios con espacios
    image_title = image_title.replace('-', ' ')
    
    return image_title

# Verificar si el usuario puede usar el comando /pato
def can_use_command(user_id):
    cursor.execute("SELECT last_used FROM command_usage WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        last_used = result[0]
        if datetime.now() - last_used < timedelta(minutes=30):
            return False
    return True

# Actualizar el tiempo de uso del comando /pato
def update_command_usage(user_id):
    cursor.execute("REPLACE INTO command_usage (user_id, last_used) VALUES (%s, %s)", (user_id, datetime.now()))
    db.commit()

# Iniciar el bot
intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

# Cargar los nombres de archivos de imágenes desde el archivo .txt en GitHub
image_files = download_image_list()

# Comando para mostrar una imagen aleatoria
@client.command()
async def pato(ctx):
    user_id = ctx.author.id
    
    # Verificar si el usuario puede usar el comando
    if not can_use_command(user_id):
        await ctx.send("Debes esperar 30 minutos antes de usar este comando nuevamente.")
        return
    
    if not image_files:
        await ctx.send('Error al cargar la lista de imágenes.')
        return
    
    # Seleccionar una imagen aleatoria de la lista
    random_image_url = random.choice(image_files)
    
    # Descargar la imagen desde la URL
    image_data = download_image(random_image_url)
    if image_data:
        # Obtener el título de la imagen desde la URL
        image_title = get_image_title(random_image_url)
        
        # Verificar si la imagen ya está en la base de datos
        cursor.execute("SELECT id FROM patos WHERE url = %s", (random_image_url,))
        pato = cursor.fetchone()
        if not pato:
            cursor.execute("INSERT INTO patos (url, title) VALUES (%s, %s)", (random_image_url, image_title))
            db.commit()
            pato_id = cursor.lastrowid
        else:
            pato_id = pato[0]
        
        # Reclamar el pato para el usuario
        cursor.execute("INSERT INTO user_patos (user_id, pato_id) VALUES (%s, %s)", (user_id, pato_id))
        db.commit()
        
        # Actualizar el tiempo de uso del comando
        update_command_usage(user_id)
        
        # Crear un embed con el título y la imagen adjunta
        embed = Embed(title=image_title, color=0xFFFF00)
        embed.set_image(url=random_image_url)
        
        # Enviar el embed con la imagen al chat
        await ctx.send(embed=embed)
    else:
        await ctx.send('Error al cargar la imagen.')

# Evento cuando el bot se conecta exitosamente
@client.event
async def on_ready():
    print(f'{client.user.name} está listo!')
    # Setea la actividad actual una vez que el bot está listo
    await client.change_presence(activity=Activity(type=ActivityType.playing, name="/pato | OnlyDucks 🦆"))

# Conectar el bot con el token proporcionado
client.run(TOKEN)
