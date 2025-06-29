from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.endpoints import router as auth_router
from app.middleware.error_handler import setup_error_handlers
from app.ping.endpoints import router as ping_router
from app.races.endpoints import router as race_router
from app.settings import settings
from app.users.endpoints import router as user_router


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

setup_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping_router, prefix="/ping", tags=["Health Check"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(race_router, prefix="/races", tags=["Race"])
app.include_router(user_router, prefix="/users", tags=["Users"])

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
