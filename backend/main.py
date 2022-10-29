import uvicorn
from app.api import login, packs, periods, styles, users
from app.api.beatport import labels
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "users",
        "description": "Only admin can create users. User can get information about itself. The user's email is unique",
    },
    {
        "name": "styles",
        "description": "The user can only work with its own styles. The user cannot see or change the styles of other "
        "users. The user can get all of its styles. The style's name is unique",
    },
    {
        "name": "periods",
        "description": "The user can only work with its own periods. The user cannot see or change the periods of "
        "other users. The user can get all of its periods. Period can start and finish in one day, "
        "but couldn't start after the last day. The period's name is unique",
    },
    {
        "name": "packs",
        "description": "Pack is the connector between the style and the period. The user can only work with their own "
        "styles and periods. You cannot create a pack with the same style and period id",
    },
    {
        "name": "labels",
        "description": "Labels are for saving beatport label's information, their IDs and names. Any user can create "
        "it. Only admin can delete it",
    },
]


def create_application() -> FastAPI:
    application = FastAPI(
        title="cLoudER Space", version="0.3.3", openapi_tags=tags_metadata
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
