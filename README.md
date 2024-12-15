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


### Async Setup

#### SQLAlchemy

- change engine, session, session maker to async versions
- functions and context manager become async
- await methods like execute, commit

#### Pytest

- needs pytest-asyncio
- tests must be marked or in pytest.ini asyncio_mode=auto
- this marks every async test as async
- pytest-asyncio doesnt work well with sqlalchemy
- common error: "RunTimeError: Task got Future attached to different loop"
- to avoid that, run everything in same event loop
- therefore, use same session maker from app (to have same pool)
- set asyncio_default_fixture_loop_scope=session in pytest.ini so fixtures use same loop
- use pytest_collection_modifyitems hook in conftest.py to use same event loop for all tests


### Alembic setup

- using `alembic init -t async <script_directory_here>` (asyncio template)
- adapt env.py to use DB URL from config and engine from DB URL
- in env.py import models and declarative base
- timestamp on version tags configuration in alembic.ini