from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes.ask import router as ask_router


app = FastAPI(
    title="AI Document Q&A API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload_router)
app.include_router(ask_router)


@app.get("/")
def root():
    return {
        "message": "AI Document Q&A API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }