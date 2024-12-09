# App

FastAPI app.
From repo root directory run `uvicorn app.app:app --reload`.

- [app.py](./app.py) app object, exception handlers, middleware
- [db/](./db/) sessions, models, and CRUD methods for database
- [api/](./api/) REST API models(=schemas) and endpoints
- [settings.py](./settings.py) basic settings, read config.json and ENV
- [exceptions.py](./exceptions.py) custom exceptions
