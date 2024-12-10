import os
from fastapi import FastAPI
from app.db import Base, sync_engine
from app.routes import job_application_routes
from app.middleware.logging_middleware import BeforeAfterLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=sync_engine)

app.add_middleware(BeforeAfterLoggingMiddleware)

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(job_application_routes.router)

@app.get("/")
async def root():
    return {"message": "Job Application Tracker Microservice"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
