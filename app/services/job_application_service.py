from sqlalchemy.orm import Session
from ..models.job_application import JobApplication
from ..models.user import User
from ..models.job_posting import JobPosting
from ..schemas.job_application_schema import JobApplicationCreate

def get_application_by_id(db: Session, application_id: int):
    return (db.query(JobApplication)
            .filter(JobApplication.application_id == application_id).first())

def get_applications_by_user_id(db: Session, user_id: int):
    return (db.query(JobApplication)
            .filter(JobApplication.user_id == user_id).all())