from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from ..db import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    application_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_postings.job_id"), nullable=False)
    status = Column(Enum("Applied", "Interviewing", "Offer", "Rejected"), default="Applied")
    application_date = Column(DateTime)
    notes = Column(String(255))

    user = relationship("User")
    job = relationship("JobPosting")
