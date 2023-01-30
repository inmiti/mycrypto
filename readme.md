
# Aplicación Web MYCRYPTO

- Programa hecho en python con el framework Flask, App MyCrypto, con motor de base de datos SQLite y API https://www.coinapi.io/.

## Instalar librerías

- Para instalar las librerías una vez dentro del entorno de python del proyecto utilizar el comando siguiente:

```
pip install -r requirements.txt
```

- Librerias utilizadas:

flask https://flask.palletsprojects.com/en/2.2.x/

dotenv https://www.dotenv.org/

WTF https://flask-wtf.readthedocs.io/en/1.0.x/

request https://requests.readthedocs.io/en/latest/#

## Ejecutar el servidor con .env

- Renombrar el archivo .env_template a .env y agregar las siguientes lineas:
```
FLASK_APP= nombre_archivo.py
FLASK_DEBUG= True | False
```
- En la terminal ejecutar el comando:
```
flask run
```

## Comando para ejecutar el servidor:
```
flask --app hello run
```

## Comando para actualizar el servidor con cambios de codigo en tiempo real

```
flask --app hello --debug run
```

## Comando especial para lanzar el servidor en un puerto diferente
- Esto se utiliza en el caso que el puerto 5000 este ocupado

```
flask --app hello run -p 5001
```

## Comando para lanzar en modo debug y con puerto cambiado
```
flask --app hello --debug run -p 5001
```

## Base de datos

- Crear base de datos mycrypto.sgqlite utilizando para ello la sentencia sql incluida en el archivo "mycrypto_create.sql", todo en el directorio "data". 

## API

