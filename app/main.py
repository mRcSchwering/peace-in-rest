from fastapi import FastAPI
from .api.v1.version import router as v1_router

app = FastAPI()
app.include_router(v1_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
