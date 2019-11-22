# Docker

Using docker images. Build base image

```
docker build -f docker/ -t alpine-python3
```

Build services with docker-compose and run them.
Exits with exit code from testing service.

```
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml up --exit-code-from test
```
