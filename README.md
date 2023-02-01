# Descripción
Api creada para servir a [ubicor-frontend](https://github.com/CrissAlvarezH/ubicor-frontend) y para sustituir la [versión legacy](https://github.com/CrissAlvarezH/ubicor-api-legacy).
El api consta de endpoint para la creación, actualización y consulta de bloques y salones dentro de una universidad, incluidas las imagenes y las ubicaciones gps.

### Stack
 - [FastApi](https://fastapi.tiangolo.com/) para la creación del api
 - [SQLAlchemy](https://www.sqlalchemy.org/) como el ORM
 - [Alembic](https://alembic.sqlalchemy.org/en/latest/) para las migraciones de la base de datos
 - [Poetry](https://python-poetry.org/) como manejador de dependencias
 - [Click](https://click.palletsprojects.com/en/8.1.x/) para la creacion de CLI `manage.py` para ejecutar comandos
 - [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) para el empaquetamiento del proyecto para **dev** y **prod**
 - [Github Actions](https://github.com/features/actions) Para la integración continua
 - [Black](https://black.readthedocs.io/en/stable/) formateador de codigo
 - [Isort](https://pycqa.github.io/isort/) formatea y organiza los imports
 - [pre-commit](https://pre-commit.com/) herramienta para instalar y ejecutar hooks de git

# Desplegar

## Producción
Para desplegar junto con el frontend y con la configuración de los dominios y el lets encrypt puede seguir los pasos del README del respositorio: [cristian-projects-server](https://github.com/CrissAlvarezH/cristian-projects-server)

## Testing
Se se desea desplegar para motivos de pruebas locales los pasos son los siguientes.

#### 1. Instalar poetry
Para esto puede seguir la [guía oficial](https://python-poetry.org/docs/#installation)

#### 2. Descargar las dependencias

    poetry install

#### 3. Variables de entorno
Clonar el archivo `.env.example`, renombrar a `.env` y cambiar los valores de cada variable por los que 
necesite usar, como las credenciales de la base de datos, por ejemplo.

#### 4. Correr comandos de inserción de data inicial
Se deben ejecutar las migraciones de la base de datos, crear un superusuario e insertar una data 
inicial para llenar la base de datos, para esto usamos el siguiente comando.

    make prestart

#### 5. Correr servidor
Corremos con el flag `--reload` para que se refresque cada que detecte un cambio en el codigo

    uvicorn app.main:app --reload

## Usando Docker
Si queremos usar docker parar en lanzamiento de la app podemos usar `docker-compose` y este lanzará, ademas del contenedor con el api,  [un contenedor con la base de datos postgres](https://hub.docker.com/_/postgres)

    docker-compose up

El comando anterior creará los contenedores necesarios y ejecutará los scripts para el funcionamiento correcto de la app.


# Preparar para desarrollo

## 1. Usar poetry para instalar las dependencias

```
# crear la carpeta .venv en la raiz del proyecto
poetry config virtualenvs.in-project true 

# instalar dependencias
poetry install

# activar environment de python
source .venv/bin/activate
```

## 2. Instalar pre-commit en git

```
pre-commit install
```

## 3. Correr proyecto en local

```
make start
```

## Usando Docker

```
# construimos la imagen
# Nota: en Mac puede ser necesario ejecutar (solo para el build)
# export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose build

# corremos la imagen de la app y de la base de datos
docker-compose up
```

Despues de ejecutar esos comandos podrás ver el siguiente output en consola

```
ubicor-api-database-1  | 2023-05-29 05:25:52.996 UTC [1] LOG:  starting PostgreSQL 14.8 on aarch64-unknown-linux-musl, compiled by gcc (Alpine 12.2.1_git20220924-r10) 12.2.1 20220924, 64-bit
ubicor-api-database-1  | 2023-05-29 05:25:52.996 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
ubicor-api-database-1  | 2023-05-29 05:25:52.997 UTC [1] LOG:  listening on IPv6 address "::", port 5432
ubicor-api-database-1  | 2023-05-29 05:25:52.999 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
ubicor-api-database-1  | 2023-05-29 05:25:53.002 UTC [52] LOG:  database system was shut down at 2023-05-29 05:25:52 UTC
ubicor-api-database-1  | 2023-05-29 05:25:53.005 UTC [1] LOG:  database system is ready to accept connections
ubicor-api-app-1       | INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
ubicor-api-app-1       | INFO  [alembic.runtime.migration] Will assume transactional DDL.
ubicor-api-app-1       | INFO  [alembic.runtime.migration] Running upgrade  -> 4f275ac0046b, create models
ubicor-api-app-1       | 
ubicor-api-app-1       | INIT create superuser
ubicor-api-app-1       | FINISH create superuser
ubicor-api-app-1       | 
ubicor-api-app-1       | INIT insert initial data
ubicor-api-app-1       | FINISH insert initial data
ubicor-api-app-1       | INFO:     Will watch for changes in these directories: ['/code']
ubicor-api-app-1       | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
ubicor-api-app-1       | INFO:     Started reloader process [1] using watchgod
ubicor-api-app-1       | INFO:     Started server process [24]
ubicor-api-app-1       | INFO:     Waiting for application startup.
ubicor-api-app-1       | INFO:     Application startup complete.
```

Lo cual indicará que el proyecto esta corriendo en el puerto 8000

# Configurar Integración Continua

## Github Actions

Para poner en funcionamiento las github actions se debe configurar los secrets

- DOCKER_PASSWORD
- DOCKER_USER
- AMAZON_SERVER_KEY

Y antes de esto la app debe estar corriendo instalada y corriendo en el server usando
[el repositorio de configuración del servidor](https://github.com/CrissAlvarezH/cristian-projects-server)

# Comandos

## Subir imagenes masivamente

Este comando nos permite suber imagenes a distintos bloques de forma masiva, para esto primer
debemos dejar las imagenes en la carpeta `app/universities/commands/ubicor_imgs` (para Ubicor)
estas imagenes las encontramos en los backups que se toman del servidor, las subcarpetas deben llevar
el nombre de los bloques, despues de esto podemos correr el siguiente comando.

```
python manage.py universities upload-unicor-imgs <domain> <user> <password>
```

Los parametros que debemos pasar son del backend al cual queremos apuntar.