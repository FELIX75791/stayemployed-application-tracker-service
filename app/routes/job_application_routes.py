from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..services.auth_service import verify_password, create_access_token, oauth2_scheme, decode_access_token
from ..schemas.job_application_schema import JobApplicationCreate, JobApplicationResponse
from ..services.job_application_service import get_application_by_id, get_applications_by_user_id
from ..dependencies import get_db, get_current_user_id

router = APIRouter()


@router.get("/applications/{application_id}", response_model=JobApplicationResponse)
def get_application_by_id(application_id: int, db: Session = Depends(get_db)):
    application = get_application_by_id(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Job application not found")
    return application


# 根据 user_id 获取用户的所有 Job Applications
@router.get("/applications", response_model=List[JobApplicationResponse])
def get_applications_by_user(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    applications = get_applications_by_user_id(db, user_id)
    if not applications:
        raise HTTPException(status_code=404, detail="No job applications found for this user")
    return applications
