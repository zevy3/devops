from fastapi import FastAPI
from src.routers.user import router as user_router

app = FastAPI(title="User Service")
app.include_router(user_router)


@app.get("/")
def root():
    return {"status": "ok"}
