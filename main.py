from fastapi import FastAPI
from config.database import engine, Base
from routes import todolistRoute, itemRoute

app = FastAPI(title="OOPLAB")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(todolistRoute.router)
app.include_router(itemRoute.router)
@app.get("/")
async def root():
    return {"data": "Приложение успешно подключено к бд"}
