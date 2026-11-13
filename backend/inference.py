from fastapi import FastAPI
from backend.api.routes import router as rt
app = FastAPI()
app.include_router(rt)