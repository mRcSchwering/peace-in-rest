# Peace-in-REST

REST API app template using [FastAPI](https://fastapi.tiangolo.com/) with [Uvicorn](https://www.uvicorn.org/)
as ASGI server, [Postgres](https://www.postgresql.org/) as database,
[SQLAlchemy](https://www.sqlalchemy.org/) for database interactions,
[Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations,
[Pytest](https://docs.pytest.org/en/stable/) for testing.

Run using [Docker](https://www.docker.com/):

```bash
docker compose build  # build images
docker compose up -d postgres app  # run database and app
docker compose run --rm migrations alembic upgrade head  # update database schema
```

Or locally using [Conda](https://anaconda.org/anaconda/conda):

```bash
conda env create -f environment.yml  # install conda environment
conda activate pir  # activate conda environment
docker compose up -d postgres  # run database server
alembic upgrade head  # update database schema
```


## Migrations

Alembic is used for migrations.
It was setup for async usage (see [Async Alembic Setup](#async-alembic-setup)).
Alembic configs and revisions are under [migrations/](./migrations/).
Revision files are prepended with the date.
So, if not more than one revision was created per day, they should be chronologically ordered.
To generate a new revision run:

```bash
docker compose up -d postgres  # run database server
alembic upgrade head  # update database schema
alembic check  # check current migration
alembic revision --autogenerate -m "<message>"  # generate new revision
```

Then manually check the generated revision file.
The autogenerate function does not detect everything (see [docs here](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)).
Then upgrade to inlcude the new revision.

```bash
alembic upgrade head  # update database schema
alembic current  # show current migration
git commit -a -m "<message>"  # commit revision
```


## Testing

### Functional Testing

There is a pytest test suite organized under [tests/functional/](./tests/functional/).
This is setup to be run with async tests (see [Async Pytest](#async-pytest)).
In [.github/workflows/dockerimage.yml](./.github/workflows/dockerimage.yml) these tests are executed from within a container.
Run them locally with:

```bash
docker compose up -d postgres  # run database server
pytest tests/functional/  # run tests
```

### Integration Testing

Under [tests/integration/](./tests/integration/) there is a python CLI.
It can be used to add sample data or run tests against a running app.
These tests are supposed to run against a deployed app.
In [.github/workflows/dockerimage.yml](./.github/workflows/dockerimage.yml) they are run from within one test container
against the app container in the same network.
Run them locally with:

```bash
docker compose build  # build images
docker compose up -d postgres app  # run database and app
docker compose run --rm migrations alembic upgrade head  # update database schema
docker compose run --rm tests python -m tests.integration --help  # see commands
docker compose run --rm tests python -m tests.integration sample_data --app-url "http://localhost:80"  # e.g. add sample data
```

### Migrations Testing

In [.github/workflows/dockerimage.yml](./.github/workflows/dockerimage.yml) `alembic check` is run
to make sure the defined database models match with the revisions.
To check locally:

```bash
docker compose up -d postgres  # run database server
alembic upgrade head  # update database schema
alembic check  # check current migration
```


## Async

### Async SQLAlchemy

The DBAPI for postgres has to be `asyncpg`.
SQLAlchemy provides async variants of `Session`, `sessionmaker`, `engine`, and their context managers.
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

### Async Pytest

Pytests need `pytest-asyncio` to execute async tests and fixtures.
Async tests can automatically be marked for asyncio by having `asyncio_mode=auto` in _pytest.ini_.

`pytest-asyncio` doesn't seem to work well by async SQLAlchemy.
Running tests naively leads to `"RunTimeError: Task got Future attached to different loop"`.
To avoid that, the test setup has to make sure everything runs in the same event loop.
So, I am using the _app_'s session maker and set all fixtures to the session loop by
having `asyncio_default_fixture_loop_scope=session` in _pytest.ini_.
But there is no such setting for the async tests themselves.
This has to be done manually with a hook `pytest_collection_modifyitems` in _conftest.py_ (according to the docs).

### Async Alembic Setup

Alembic has a async setup command `alembic init -t async ...`.
_env.py_ has to be edited to load ORM mappings and the database URL from _app_.
The `connectable` can be created with `create_async_engine` with a `NullPool`.
I also edited _alembic.ini_ to include a timestamp in the migration file, so that they are easier to find.

### Async FastAPI Uvicorn

FastAPI offers a CLI that starts uvicorn to serve the app.
This CLI has a `--workers` argument to start multiple processes at once.
Setting this argument (more than 1 process) breaks the app.
There will be `connection refused` errors if many requests are comming in.
I added concurrency tests to [tests/integration/](./tests/integration/).
Probably the web server doesn't serve multiple processes correctly.

I assume serving the app with gunicorn would work fine.
But this means, one has to make the decision of whether to use asyncio or multiple processes.
Both wouldn't work.
