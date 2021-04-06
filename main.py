import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app import settings
from app.routers import universe, status

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
]

# Start the FastAPI
app = FastAPI(
    title="PrunData API",
    description='PrunData API for Prosperous Universe',
    version='1.0',
    openapi_tags=tags_metadata
)

# Setup Cross Origin Scripting to allow requests from Apex
app.add_middleware(CORSMiddleware, allow_origins=['*'])

# Include the routers
app.include_router(universe.router, prefix='/universe')
app.include_router(status.router, prefix='/status')

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
