from fastapi import FastAPI

from app.routes.upload import router as upload_router

app = FastAPI(
    title="AI Document Q&A API",
    version="1.0.0"
)

app.include_router(upload_router)


@app.get("/")
def root():
    return {"message": "AI Document Q&A API is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}