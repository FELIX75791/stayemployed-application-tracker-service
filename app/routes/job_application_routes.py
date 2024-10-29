from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List
from ..schemas.job_application_schema import JobApplicationResponse, JobApplicationUpdate, JobApplicationCreate
from ..services.job_application_service import (
    get_application_by_app_id,
    get_applications_by_user_email,
    create_job_application,
    update_job_application,
    delete_application
)
from ..dependencies import get_current_user_email
from ..db import get_async_db, get_sync_db

router = APIRouter()

@router.get("/my_applications/{application_id}", response_model=JobApplicationResponse)
def get_user_application(
    application_id: int,
    db: Session = Depends(get_sync_db),
    user_email: str = Depends(get_current_user_email)
):
    application = get_application_by_app_id(db, application_id)
    if application is None or application.user_email != user_email:
        raise HTTPException(status_code=404, detail="Job application not found")
    return application

@router.get("/my_applications", response_model=List[JobApplicationResponse])
def get_applications_by_user(
    page: int = 1,
    user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_sync_db)
):
    applications = get_applications_by_user_email(db, user_email, page)
    if not applications:
        raise HTTPException(status_code=404, detail="No job applications found for this user")
    return applications

@router.post("/my_applications", response_model=JobApplicationResponse)
async def create_application(
    application_data: JobApplicationCreate,
    db: AsyncSession = Depends(get_async_db),
    user_email: str = Depends(get_current_user_email)
):
    new_application = await create_job_application(db, application_data, user_email)
    return new_application

@router.patch("/my_applications/{application_id}", response_model=JobApplicationResponse)
async def update_application_route(
    application_id: int,
    update_data: JobApplicationUpdate,
    db: AsyncSession = Depends(get_async_db),
    user_email: str = Depends(get_current_user_email)
):
    updated_application = await update_job_application(db, application_id, update_data, user_email)
    if not updated_application:
        raise HTTPException(status_code=404, detail="Failed to update application")
    return updated_application

@router.delete("/my_applications/{application_id}")
async def delete_application_route(
    application_id: int,
    db: AsyncSession = Depends(get_async_db),
    user_email: str = Depends(get_current_user_email)
):
    success = await delete_application(db, application_id, user_email)
    if not success:
        raise HTTPException(status_code=404, detail="Failed to delete application")
    return {"detail": "Job application deleted successfully"}
