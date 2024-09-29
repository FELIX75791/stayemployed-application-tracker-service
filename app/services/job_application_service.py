from sqlalchemy.orm import Session
from ..models.job_application import JobApplication
from ..models.user import User
from ..models.job_posting import JobPosting
from ..schemas.job_application_schema import JobApplicationCreate

def get_application_by_app_id(db: Session, application_id: int):
    return (db.query(JobApplication)
            .filter(JobApplication.application_id == application_id).first())

def get_applications_by_user_email(db: Session, user_email: str):
    return (db.query(JobApplication)
            .filter(JobApplication.user_email == user_email).all())
