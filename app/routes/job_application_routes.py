from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..services.auth_service import verify_password, create_access_token, oauth2_scheme, decode_access_token
from ..schemas.job_application_schema import JobApplicationCreate, JobApplicationResponse
from ..services.job_application_service import get_application_by_app_id, get_applications_by_user_email
from ..dependencies import get_db, get_current_user_email

router = APIRouter()


@router.get("/my_applications/{application_id}", response_model=JobApplicationResponse)
def get_user_application(application_id: int, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    application = get_application_by_app_id(db, application_id)
    if application is None or application.user_email != user_email:
        raise HTTPException(status_code=404, detail="Job application not found")
    return application


@router.get("/my_applications", response_model=List[JobApplicationResponse])
def get_applications_by_user(user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    applications = get_applications_by_user_email(db, user_email)
    if not applications:
        raise HTTPException(status_code=404, detail="No job applications found for this user")
    return applications
