from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.routes import api_router


def custom_generate_unique_id(route: APIRoute):
    """Generate id function more clean for fastapi autogenerate documentation

    Its allow use the openapi.son to create api clients using tools
    like openapi-typescript-codegen and get api method names more cleaned
    """
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS.split(",")
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router, prefix="/api/v1")
