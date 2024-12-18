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

# e2e tests (in 2 terminals to see logs)
docker compose build
docker compose up postgres app
...
docker compose run --rm migrations alembic upgrade head
docker compose run --rm tests python -m tests.e2e test concurrency
```


### Async

#### SQLAlchemy

The DBAPI for postgres has to be `asyncpg`.
SQLAlchemy are async variants of `Session`, `sessionmaker`, `engine`, and their context managers.
Practically, this means `execute()` and `commit()` have to be awaited.
This also means lazy loading attributes doesn't work as before.
I set `relationship(lazy="raise")` so that one has to fetch all attributes explicitly (better anyway).
The session maker has `expire_on_commit=False`, so that ORM objects can be used after committing a session.

A session uses one event loop and is not threadsafe.
So within a session everything should run in sequence.
Which means the asynchronous execution comes to play on the request level only
(e.g. one request can be handled while another is waiting for the database to respond).

When using the SQLAlchemy Core API ORM-sided features don't always work.
E.g. `relationship(..., cascade="delete")` doesn't actually trigger on delete.
Instead I have to use the database features, i.e. `ForeignKey(..., ondelete="CASCADE")`.

#### Pytest

Pytests need `pytest-asyncio` to execute async tests and fixtures.
Async tests can automatically be marked for asyncio by having `asyncio_mode=auto` in _pytest.ini_.

`pytest-asyncio` doesn't seem to work well by async SQLAlchemy.
Running tests naively leads to `"RunTimeError: Task got Future attached to different loop"`.
To avoid that, the test setup has to make sure everything runs in the same event loop.
So, I am using the _app_'s session maker and set all fixtures to the session loop by
having `asyncio_default_fixture_loop_scope=session` in _pytest.ini_.
But there is no such setting for the async tests themselves.
This has to be done manually with a hook `pytest_collection_modifyitems` in _conftest.py_ (according to the docs).


### Alembic setup

Alembic has a async setup command `alembic init -t async ...`.
_env.py_ has to be edited to load ORM mappings and the database URL from _app_.
The `connectable` can be created with `create_async_engine` with a `NullPool`.
I also edited _alembic.ini_ to include a timestamp in the migration file, so that they are easier to find.


### FastAPI

FastAPI offers a CLI that starts uvicorn to serve the app.
This CLI has a `--workers` argument to start multiple processes at once.
Setting this argument (more than 1 process) breaks the app.
There will be `connection refused` errors if many requests are comming in.
I added concurrency tests to [tests/e2e/](./tests/e2e/).
Probably the web server doesn't serve multiple processes correctly.

I assume serving the app with gunicorn would work fine.
But this means, one has to make the decision of whether to use asyncio or multiple processes.
Both wouldn't work.
