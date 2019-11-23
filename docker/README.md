# Docker

Build alpine-python3 base image and push it to github registry.

```
docker build -f docker/Dockerfile_base -t alpine-python3 docker/

docker login docker.pkg.github.com --username mrcschwering
docker tag alpine-python3 docker.pkg.github.com/mrcschwering/peace-in-rest/alpine-python3:latest
docker push docker.pkg.github.com/mrcschwering/peace-in-rest/alpine-python3:latest
```

Build app and test services with docker-compose.
Start app with database server and run tests against app.
Exits with exit code from tests.

```
docker-compose -f docker/docker-compose-test.yml build
docker-compose -f docker/docker-compose-test.yml up --exit-code-from test
```
