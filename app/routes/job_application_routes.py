from fastapi import APIRouter, Depends, HTTPException, status, Response, BackgroundTasks
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


@router.get("/my_applications/{application_id}", response_model=JobApplicationResponse, status_code=status.HTTP_200_OK)
def get_user_application(
        application_id: int,
        db: Session = Depends(get_sync_db),
        user_email: str = Depends(get_current_user_email)
):
    application = get_application_by_app_id(db, application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job application not found")
    if application.user_email != user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Permitted")

    links = [
        {"rel": "self", "href": f"/my_applications/{application_id}", "method": "GET"},
        {"rel": "update", "href": f"/my_applications/{application_id}", "method": "PATCH"},
        {"rel": "delete", "href": f"/my_applications/{application_id}", "method": "DELETE"},
    ]

    response = JobApplicationResponse(**application.__dict__, links=links)
    return response

@router.get("/my_applications", response_model=List[JobApplicationResponse], status_code=status.HTTP_200_OK)
def get_applications_by_user(
        page: int = 1,
        user_email: str = Depends(get_current_user_email),
        db: Session = Depends(get_sync_db)
):
    applications = get_applications_by_user_email(db, user_email, page)
    if not applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No job applications found for this user")

    responses = []
    for app in applications:
        links = [
            {"rel": "self", "href": f"/my_applications/{app.application_id}", "method": "GET"},
            {"rel": "update", "href": f"/my_applications/{app.application_id}", "method": "PATCH"},
            {"rel": "delete", "href": f"/my_applications/{app.application_id}", "method": "DELETE"},
        ]
        responses.append(JobApplicationResponse(**app.__dict__, links=links))

    return responses

@router.post("/my_applications", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    response: Response,
        application_data: JobApplicationCreate,
        db: AsyncSession = Depends(get_async_db),
        user_email: str = Depends(get_current_user_email)
):
    new_application = await create_job_application(db, application_data, user_email)

    response.headers["Link"] = f'</my_applications/{new_application.application_id}>; rel="self"'

    links = [
        {"rel": "self", "href": f"/my_applications/{new_application.application_id}", "method": "GET"},
        {"rel": "update", "href": f"/my_applications/{new_application.application_id}", "method": "PATCH"},
        {"rel": "delete", "href": f"/my_applications/{new_application.application_id}", "method": "DELETE"},
    ]
    return JobApplicationResponse(**new_application.__dict__, links=links)


@router.patch("/my_applications/{application_id}", response_model=JobApplicationResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_application_route(
        application_id: int,
        update_data: JobApplicationUpdate,
        db: AsyncSession = Depends(get_async_db),
        user_email: str = Depends(get_current_user_email)
):
    updated_application = await update_job_application(db, application_id, update_data, user_email)
    if not updated_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to update application")

    links = [
        {"rel": "self", "href": f"/my_applications/{application_id}", "method": "GET"},
        {"rel": "delete", "href": f"/my_applications/{application_id}", "method": "DELETE"},
    ]
    return JobApplicationResponse(**updated_application.__dict__, links=links)


@router.delete("/my_applications/{application_id}", status_code=status.HTTP_200_OK)
async def delete_application_route(
        application_id: int,
        db: AsyncSession = Depends(get_async_db),
        user_email: str = Depends(get_current_user_email)
):
    success = await delete_application(db, application_id, user_email)
    if not success:
        raise HTTPException(status_code=404, detail="Failed to delete application")

    response = {
        "detail": "Job application deleted successfully",
        "links": [
            {"rel": "create", "href": "/my_applications", "method": "POST"},
            {"rel": "list", "href": "/my_applications", "method": "GET"},
        ]
    }
    return response