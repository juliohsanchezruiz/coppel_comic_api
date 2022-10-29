# Api Comic
# Python-Flask-with-Docker-Compose

Ejecute la instrucción Docker Compose para iniciar Api Comic (`Python`, `Flask`).

```bash
docker-compose up -d
```

## Modificar credenciales para Marvel Comic Server

Actualice el archivo `.env` (variables de entorno) con sus credenciales específicas.

```bash
WEB_HOST=api_comic

MARVEL_PUBLIC_KEY=********************************
MARVEL_PRIVATE_KEY=***********************
MARVEL_URL="https://gateway.marvel.com:443"
MARVEL_PATH_COMICS="v1/public/comics"
MARVEL_PATH_CHARACTER="v1/public/characters"
```

## Otras instrucciones

#### Remover Volumen
Tenemos dos formas de eliminar nuestros volúmenes con Docker.

Primero está usando el comando `prune`.

```bash
docker volume prune -f
```

El segundo es usar el comando actual `volume rm` con `-f` como parámetro.

```bash
docker volume rm $(docker volume ls -q)
```

#### Limpie el volumen de Cache para Python

```bash
rm -rf app/__pycache__/
```

#### Eliminar caché en el sistema Docker

```bash
docker system prune -a -f && docker builder prune -a -f
```

### Recrear `web_comic` de contenedor

```bash
docker-compose up --build --force-recreate --no-deps -d web_comic
```

### Mostrar registros de ejecución de API

```bash
docker logs --tail 1000 -f api_comic
```
