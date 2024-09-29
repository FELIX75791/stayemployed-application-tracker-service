from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from ..db import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    job_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    location = Column(String(255))
    description = Column(String(255))
    posted_date = Column(DateTime)
    apply_url = Column(String(255))
