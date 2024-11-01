from fastapi import FastAPI
from app.db import Base, sync_engine
from app.routes import job_application_routes
from app.middleware.logging_middleware import BeforeAfterLoggingMiddleware
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=sync_engine)

app.add_middleware(BeforeAfterLoggingMiddleware)
app.include_router(job_application_routes.router)

@app.get("/")
async def root():
    return {"message": "Job Application Tracker Microservice"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
