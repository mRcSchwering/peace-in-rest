# Peace-in-REST

REST API app template using FastAPI and SQLAlchemy.

```
# start app locally
fastapi dev app/main.py

# build docker image for app
docker build -f docker/Dockerfile --target app -t myapp . 

# run app alone in docker container
docker run -d --rm -p 80:80 myapp

# generate migration from code
alembic revision --autogenerate -m "init"

# upgrade to most recent migration
alembic upgrade head

# show current migration
alembic current

# fails if code has changed that is not reflected in migration
alembic check
```


### Async Setup

#### SQLAlchemy

- change engine, session, session maker to async versions
- functions and context manager become async
- await methods like execute, commit
- should use `expire_on_commit=False` and eagerly load everything needed
- set `relationship(lazy="raise")` to avoid lazy loading
- within one session everything must be concurrent (session is uses 1 event loop)
- ORM-sided feature dont always work (e.g. `relationship(.."delete")` doesn't work)
- should make use of database features instead (e.g. `ForeignKey("user.id", ondelete="CASCADE")`)

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


### Workers geht nicht

- tldr: `fastapi run` with multiple `workers` doesnt work (at least not with this async setup)
- at least together with async and using the normal `fastapi` cli it doesnt work
- during concurrency test, it raises `connection refused`
- I guess the web server used by `fastapi` doesn't serve to the multiple processes correctly