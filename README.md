# Despliegue de FastAPI + PostgreSQL en Render

Este documento describe el proceso completo de despliegue de una aplicación python en Render.

Esta aplicación web será creada con Python, teniendo una base de datos en PostgreSQL. Usaremos Jinja2 para hacer las plantillas, y aunque en partes anteriores hemos usado Uvicorn, en 
esta parte usaremos Render para el despliegue.

---

## Estructura del proyecto

```
.
├── Dockerfile
├── Docker-compose.yml
├── requirements.txt
├── src/
│   ├── main.py
│   ├── data/
│   │   └── db.py
│   ├── models/
│   │   └── libro.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── libros_detalle.html
│   │   └── libros.html
│   └── static/
│       └── static.html
```
La estructura del proyecto divide los requisitos y los archivos Docker por un lado, mientras que el programa, la estructura del modelo,
junto a las plantillas Jinja y los datos, se encuentran en src.

---

## Dockerfile

Render utiliza el `Dockerfile` para construir la aplicación:

```dockerfile
# Use the official Python base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY ./src /app

# Expose the port on which the application will run
EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```
---
## Docker-compose.yml

Aunque en esta parte del proyecto no se ha usado, esta es la estructura del docker-compose

```yaml
name: fastapi-libros-postgre

services:
  fastapi-db:
    image: postgres:16
    container_name: fastapi-db-libros
    environment:
      POSTGRES_DB: librosdb
      POSTGRES_USER: quevedo
      POSTGRES_PASSWORD: 1234
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U quevedo -d librosdb"]
      interval: 5s
      timeout: 5s
      retries: 10

  fastapi-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi-app-libros
    restart: always
    ports:
      - "8000:8000"
    depends_on:
      fastapi-db:
        condition: service_healthy
```



---

## Base de datos PostgreSQL 

Para crear la aplicación, primero crearemos la base de datos

1. Crearemos un **PostgreSQL Service** en Render, ya que es una de las plantillas de creación dentro de los proyectos de render.
2. Introducimos el usuario y el nombre de la base de datos, render genera la contraseña y la URL de la base de datos.

---

## Modificación de la aplicación

Por el funcionamiento de render, modificamos el archivo db.py en la URL. Por lo realizado antes la url se ve tal que así

```python
DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True)

```

Sin embargo la he modificado para que se vea tal que así

```python
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL,echo=True,pool_pre_ping=True)
```
El motivo de dirigirlo a "DATABASE_URL" será explicado en el siguiente paso.

---

## Aplicación en Render

Para subir la aplicación a Render utilizaremos Git. El motivo de utilizar git es que render entre sus plantillas, permite que la de aplicaciones web
sea introducida desde Git, siendo que en este caso usaremos GitHub. 

La subida de la aplicación es bastante sencilla y al implantar deberemos añadir una variable de entorno. Dicha variable de entorno será la URL de la
base de datos mencionada en la creación de la Base de Datos en Render, a la cual le asignaremos el nombre DATABASE_URL, el cual es por el que será reconocido
en la aplicación.

Siendo, que una vez aplicado este tándem que la aplicación funcionará correctamente, siendo posible desplegarla en cualquier navegador con internet.

