from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    applied = "Applied"
    interviewing = "Interviewing"
    offer = "Offer"
    rejected = "Rejected"

class JobApplicationCreate(BaseModel):
    user_id: int
    job_id: int
    application_date: datetime
    notes: str

class JobApplicationResponse(BaseModel):
    application_id: int
    user_id: int
    job_id: int
    status: StatusEnum
    application_date: datetime
    notes: str

    class Config:
        orm_mode = True
