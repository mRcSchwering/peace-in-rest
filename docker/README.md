# Docker

Using docker images. Build separately.

```
docker build -f docker/ -t alpine-python3
docker build -f docker/Dockerfile_app -t app .
docker build -f docker/Dockerfile_test -t test_app .
```

With docker-compose.

```
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml up
```
