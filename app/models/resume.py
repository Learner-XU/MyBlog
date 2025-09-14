from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum


class SectionType(enum.Enum):
    personal_info = "personal_info"
    education = "education"
    experience = "experience"
    skills = "skills"
    projects = "projects"


class ResumeSection(Base):
    __tablename__ = "resume_sections"

    id = Column(Integer, primary_key=True, index=True)
    section_type = Column(Enum(SectionType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    order_index = Column(Integer, default=0, index=True)
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ResumeSection(id={self.id}, type='{self.section_type.value}', title='{self.title}')>"