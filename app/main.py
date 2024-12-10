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
origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific IP (127.0.0.1) with all ports
    allow_credentials=True,             # Allow credentials (e.g., cookies, authorization headers)
    allow_methods=["POST"],                # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                # Allow all HTTP headers
)

# Include API routes
app.include_router(job_application_routes.router)

@app.get("/")
async def root():
    return {"message": "Job Application Tracker Microservice"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
