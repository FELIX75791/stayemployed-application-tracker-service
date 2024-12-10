from sqlalchemy import Column, Integer, String, DateTime, Enum
from ..db import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    application_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(50), nullable=False)
    job_url = Column(String(100), nullable=False)
    status = Column(Enum("Applied", "Interviewing", "Offer", "Rejected"), default="Applied")
    resume_url = Column(String(100))
    application_date = Column(DateTime)
    notes = Column(String(255))