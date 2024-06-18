# Cuackdae

**Bot de rolls similar a Muade, pero de Patos.**

![image](https://github.com/matiasdante/cuackdae/assets/70301149/f7cc6f92-7b70-4e78-b19f-46180340932f)

## Indice

* [Introducción](#Introduccion)
* [Funcionalidades](#Funcionalidades)
* [Instalación](#Instalacion)
* [Uso](#Uso)

## Introducción

Somos desarrolladores de DCS que decidieron crear una proyecto de un bot que rolee patos de goma por siemple amor al arte y a los patos <3

Este proyecto es para uso exclusivo de trabajadores de DCS

** Rolea unos patos en un chat de discord del servidor oficial de DCS en discord. **

## Funcionalidades

* **Cuack-1** Toma los datos directamente desde este repositorio de github en un archivo txt que almacena todas las url's
* **Cuack-2:** Con el comando principal comienza a rolear un pato aleatorio y da el nombre y la foto del pato como mensaje enved.
* **Cuack-3** Perfectamente sujeto a mejores y actualizaciones sensillas de aplicar.

## Instalación

Para instalar este proyecto, sigue estos pasos:

1. Clona el repositorio:

```bash
git clone https://github.com/matiasdante/cuackdae.git
```
2. Instala dependencias:

```bash
pip3 install -r requirementes.txt
```
3. Cambiar el nombre del example.env
```bash
example.env --> .env
```

4. Lanza el comando:

```bash
nohup python3 -m cuackdae.py &
```

## Uso

* Ingresamos a al canal de discord de cuackdae
* Escribimos el comando /pato
* Disfrutar


## Adicionar base de datos

Utilizaremos MYSQL 

```bash
sudo apt install mysql-server
```

## Crear Base de Datos

```bash

CREATE DATABASE PATOS;


CREATE TABLE IF NOT EXISTS patos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_patos (
    user_id BIGINT NOT NULL,
    pato_id INT NOT NULL,
    claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pato_id) REFERENCES patos(id)
);

CREATE TABLE IF NOT EXISTS command_usage (
    user_id BIGINT NOT NULL,
    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

Agregaremos al código lo siguiente
```bash

import mysql.connector

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
```
