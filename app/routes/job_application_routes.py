from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.job_application_schema import JobApplicationUpdate, JobApplicationCreate, JobApplicationResponse
from ..services.job_application_service import (get_application_by_app_id, get_applications_by_user_email,
                                                create_job_application, update_job_application, delete_application)
from ..dependencies import get_db, get_current_user_email

router = APIRouter()


@router.post("/my_applications", response_model=JobApplicationResponse)
def create_application(application_data: JobApplicationCreate, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    new_application = create_job_application(db, application_data, user_email)
    return new_application


@router.get("/my_applications/{application_id}", response_model=JobApplicationResponse)
def get_user_application(application_id: int, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    application = get_application_by_app_id(db, application_id)
    if application is None or application.user_email != user_email:
        raise HTTPException(status_code=404, detail="Job application not found")
    return application


@router.get("/my_applications", response_model=List[JobApplicationResponse])
def get_applications_by_user(page: int = 1, user_email: str = Depends(get_current_user_email), db: Session = Depends(get_db)):
    applications = get_applications_by_user_email(db, user_email, page)
    if not applications:
        raise HTTPException(status_code=404, detail="No job applications found for this user")
    return applications


@router.patch("/my_applications/{application_id}", response_model=JobApplicationResponse)
def update_application_route(application_id: int, update_data: JobApplicationUpdate, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
    application = get_application_by_app_id(db, application_id)
    if not application or application.user_email != user_email:
        raise HTTPException(status_code=404, detail="Job application not found")

    updated_application = update_job_application(db, application_id, update_data)
    if not updated_application:
        raise HTTPException(status_code=404, detail="Failed to update application")
    return updated_application


@router.delete("/my_applications/{application_id}")
def delete_application_route(application_id: int, db: Session = Depends(get_db),
                             user_email: str = Depends(get_current_user_email)):
    application = get_application_by_app_id(db, application_id)
    if application is None or application.user_email != user_email:
        raise HTTPException(status_code=404, detail="Job application not found")

    success = delete_application(db, application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Failed to delete application")
    return {"detail": "Job application deleted successfully"}