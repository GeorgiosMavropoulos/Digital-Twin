from fastapi import FastAPI
from backend.api.routes import router as rt
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

##allow requests on other servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://digital-twin-dqlo.onrender.com'],
    allow_methods=["https://digital-twin-trfp.vercel.app/"],
    allow_headers=["*"],
)
app.include_router(rt)