## Description

REST API made in Flask/Python for Energy Devices


## Deployment with Docker

```bash
# Nota, el archivo .env no se debe incluir en el repositorio en un proyecto en producción
$ docker-compose up -d
```

## Manual Deployment

```bash
# Create virtualenv
$ virtualenv venv
```

```bash
# install requirements, but first enter environment, .venv/scripts/active
$ pip install -r requirements
```

# Dump mysql .sql file in a working database, change credentials if need in .env file

```bash
# run python app
$ python app.py
```

## Documentation

```bash
# Open swagger in browser to view Documentation
$ http://localhost:8000/api/
