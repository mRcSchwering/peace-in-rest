# Peace-in-REST

REST API app template using FastAPI and SQLAlchemy.

```
fastapi dev app/main.py

docker build -f docker/Dockerfile -t app . 

docker run -d --rm -p 80:80 app

pytest test
```

- [app/](./app/) actual app
- [test/](./test/) tests for app
- [docker/](./docker/) docker and docker-compose files
- [.github/workflows/](./.github/workflows/) simple build-test-release for github
