from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from config import variables
from routers import books, users

app = FastAPI()

app.include_router(books.router)
app.include_router(users.router)

origins = [
    'http://localhost',
    'http://localhost:4200'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_index():
    return {"success": True, "data": "Hello, API!"}


def get_custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=variables.API_TITLE,
        version=variables.API_VERSION,
        description=variables.API_DESCRIPTION,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = get_custom_openapi
