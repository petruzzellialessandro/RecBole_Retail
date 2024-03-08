from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from routes import main

def create_app():
    app = FastAPI(
        title="Recbole Retail",
        description="Recommendation System for Retail Industry",
        version="1.0"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes registration
    app.include_router(main)

    return app
