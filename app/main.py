from fastapi import FastAPI
from app.db import Base, engine
from app.routes import job_application_routes
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(job_application_routes.router)

@app.get("/")
async def root():
    return {"message": "Job Application Tracker Microservice"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
