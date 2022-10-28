import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import login, users, styles, periods, packs
from app.api.beatport import labels


def create_application() -> FastAPI:
    application = FastAPI(
        title="cLoudER Space",
        version="0.3.3"
    )
    application.include_router(users.router, prefix="/users", tags=["users"])
    application.include_router(styles.router, prefix="/styles", tags=["styles"])
    application.include_router(periods.router, prefix="/periods", tags=["periods"])
    application.include_router(packs.router, prefix="/packs", tags=["packs"])
    application.include_router(labels.router, prefix="/labels", tags=["labels"])
    application.include_router(login.router, tags=["login"])
    application.add_middleware(
        CORSMiddleware,
        # allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
        # allow_origins=settings.ALLOWED_ORIGINS,
        # TODO: Correct CORS rules
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "OPTIONS", "DELETE"],
        allow_headers=["*"],
    )
    return application


app = create_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
