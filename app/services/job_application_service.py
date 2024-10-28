from datetime import datetime

from sqlalchemy.orm import Session
from ..models.job_application import JobApplication
from ..schemas.job_application_schema import JobApplicationCreate, JobApplicationUpdate

def create_job_application(db: Session, application_data: JobApplicationCreate, user_email: str):
    new_application = JobApplication(
        user_email=user_email,
        application_date=datetime.utcnow(),
        **application_data.dict())
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

def get_application_by_app_id(db: Session, application_id: int):
    return (db.query(JobApplication)
            .filter(JobApplication.application_id == application_id).first())

def get_applications_by_user_email(db: Session, user_email: str, page: int):
    page_size = 10
    offset = (page - 1) * page_size
    applications = (db.query(JobApplication)
                    .filter(JobApplication.user_email == user_email)
                    .offset(offset).limit(page_size).all())
    return applications

def update_job_application(db: Session, application_id: int, update_data: JobApplicationUpdate):
    application = db.query(JobApplication).filter(JobApplication.application_id == application_id).first()
    if application:
        if update_data.status is not None:
            application.status = update_data.status
        if update_data.notes is not None:
            application.notes = update_data.notes
        db.commit()
        db.refresh(application)
        return application
    return None


def delete_application(db: Session, application_id: int):
    application = db.query(JobApplication).filter(JobApplication.application_id == application_id).first()
    if application:
        db.delete(application)
        db.commit()
        return True
    return False