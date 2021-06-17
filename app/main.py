from fastapi import FastAPI
from app.api.file_registration import filesregister
from app.api.db import metadata, database, engine
from app.api.settings import getConfig


cnf = getConfig()

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(
    filesregister, prefix=cnf.APP_CONFIG.prefix, tags=cnf.APP_CONFIG.tags
)
