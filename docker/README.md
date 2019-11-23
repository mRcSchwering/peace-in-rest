# Docker

Build alpine-python3 base image.

```
docker build -f docker/Dockerfile_base -t alpine-python3 docker/
```

Build app and test services with docker-compose.
Start app with database server and run tests against app.
Exits with exit code from tests.

```
docker-compose -f docker/docker-compose-test.yml build
docker-compose -f docker/docker-compose-test.yml up --exit-code-from test
```
