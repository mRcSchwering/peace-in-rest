# Peace-in-REST

REST API app template using FastAPI and SQLAlchemy.

```
fastapi dev app/main.py

docker build -f docker/Dockerfile -t myapp . 

docker run -d --rm -p 80:80 myapp

docker compose -f docker/docker-compose.yaml up

alembic revision --autogenerate -m "init"

alembic upgrade head

alembic current
```


### Alembic setup

- use config from app for DB_URL
- import models and declarative base