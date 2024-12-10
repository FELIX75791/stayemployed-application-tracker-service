from datetime import datetime

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.job_application import JobApplication
from ..schemas.job_application_schema import JobApplicationCreate, JobApplicationUpdate
import asyncio

lock = asyncio.Lock()

def get_application_by_app_id(db: Session, application_id: int):
    result = db.execute(select(JobApplication).filter(JobApplication.application_id == application_id))
    return result.scalars().first()

def get_applications_by_user_email(db: Session, user_email: str, page: int):
    page_size = 10
    offset = (page - 1) * page_size
    result = db.execute(
        select(JobApplication)
        .filter(JobApplication.user_email == user_email)
        .offset(offset)
        .limit(page_size)
    )
    return result.scalars().all()

def get_total_application_count_by_user_email(db: Session, user_email: str) -> int:
    total_count = db.execute(
        select(func.count())
        .select_from(JobApplication)
        .filter(JobApplication.user_email == user_email)
    ).scalar_one()
    return total_count

async def create_job_application(db: AsyncSession, application_data: JobApplicationCreate, user_email: str):
    async with lock:
        new_application = JobApplication(
            user_email=user_email,
            application_date=datetime.utcnow(),
            **application_data.dict()
        )
        db.add(new_application)
        await db.commit()
        await db.refresh(new_application)
        return new_application

async def update_job_application(db: AsyncSession, application_id: int, update_data: JobApplicationUpdate, user_email: str):
    async with lock:
        application = await db.execute(select(JobApplication).filter(JobApplication.application_id == application_id))
        application = application.scalars().first()
        if not application or application.user_email != user_email:
            return None

        if application:
            if update_data.status is not None:
                application.status = update_data.status
            if update_data.notes is not None:
                application.notes = update_data.notes
            if update_data.resume_url is not None:
                application.resume_url = update_data.resume_url
            await db.commit()
            await db.refresh(application)
            return application
        return None

async def delete_application(db: AsyncSession, application_id: int, user_email: str):
    async with lock:
        application = await db.execute(select(JobApplication).filter(JobApplication.application_id == application_id))
        application = application.scalars().first()
        if not application or application.user_email != user_email:
            return None

        application = await db.get(JobApplication, application_id)
        if application:
            await db.delete(application)
            await db.commit()
            return True
        return False
