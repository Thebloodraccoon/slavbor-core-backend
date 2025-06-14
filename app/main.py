from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.ping import router as ping_router
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.Base.metadata.create_all(bind=settings.engine)
    yield
    print("Application is shutting down.")


app = FastAPI(
    lifespan=lifespan,
    version=settings.APP_VERSION,
    description=settings.APP_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping_router, prefix="/ping", tags=["Health Check"])


if __name__ == "__main__":
    if settings.STAGE == "prod":
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=8000,
            reload=True,
        )
    else:
        uvicorn.run("app.main:app", host=settings.HOST, port=8000, reload=True)
