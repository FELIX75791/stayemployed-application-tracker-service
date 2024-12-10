from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class StatusEnum(str, Enum):
    applied = "Applied"
    interviewing = "Interviewing"
    offer = "Offer"
    rejected = "Rejected"

class JobApplicationCreate(BaseModel):
    job_url: str
    status: StatusEnum = StatusEnum.applied
    resume_url: Optional[str]
    notes: Optional[str]

class JobApplicationResponse(BaseModel):
    application_id: int
    user_email: str
    job_url: str
    status: StatusEnum
    resume_url: Optional[str]
    application_date: datetime
    notes: Optional[str]
    links: List[Dict[str, str]]

    class Config:
        orm_mode = True

class JobApplicationUpdate(BaseModel):
    status: Optional[StatusEnum]
    resume_url: Optional[str]
    notes: Optional[str]

    class Config:
        orm_mode = True