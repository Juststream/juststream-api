import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import videos_router, blogs_router, reddit_router, livescore_router

ENVIRONMENT = os.environ.get("ENVIRONMENT")
LOCAL = os.environ.get("LOCAL")

app = FastAPI(
    title="JustStream API",
    description="JustStream API",
    version="1.0.0",
)

origins = [
    "http://juststream.live",
    "https://juststream.live",
    "http://www.juststream.live",
    "https://www.juststream.live",
    "http://dev.juststream.live",
    "https://dev.juststream.live",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [videos_router, blogs_router, reddit_router, livescore_router]:
    app.include_router(router.router)


@app.get('/health')
async def health():
    return {'status': 'OK'}
