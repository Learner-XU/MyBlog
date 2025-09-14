from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List
from app.models.resume import SectionType


class ResumeSectionBase(BaseModel):
    section_type: SectionType
    title: str
    content: Optional[str] = None
    order_index: int = 0
    is_visible: bool = True


class ResumeSectionCreate(ResumeSectionBase):
    pass


class ResumeSectionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order_index: Optional[int] = None
    is_visible: Optional[bool] = None


class ResumeSection(ResumeSectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeData(BaseModel):
    personal_info: List[ResumeSection]
    education: List[ResumeSection]
    experience: List[ResumeSection]
    skills: List[ResumeSection]
    projects: List[ResumeSection]