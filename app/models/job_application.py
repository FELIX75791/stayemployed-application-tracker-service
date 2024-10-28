from sqlalchemy import Column, Integer, String, DateTime, Enum
from ..db import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    application_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(50), nullable=False)
    job_id = Column(Integer, nullable=False)
    status = Column(Enum("Applied", "Interviewing", "Offer", "Rejected"), default="Applied")
    application_date = Column(DateTime)
    notes = Column(String(255))