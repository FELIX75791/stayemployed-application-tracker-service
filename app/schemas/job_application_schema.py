from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    applied = "Applied"
    interviewing = "Interviewing"
    offer = "Offer"
    rejected = "Rejected"

class JobApplicationCreate(BaseModel):
    job_id: int
    status: StatusEnum = StatusEnum.applied
    resume_url: Optional[str]
    notes: Optional[str]

class JobApplicationResponse(BaseModel):
    application_id: int
    user_email: str
    job_id: int
    status: StatusEnum
    resume_url: Optional[str]
    application_date: datetime
    notes: Optional[str]

class JobApplicationUpdate(BaseModel):
    status: Optional[StatusEnum]
    resume_url: Optional[str]
    notes: Optional[str]

    class Config:
        orm_mode = True
