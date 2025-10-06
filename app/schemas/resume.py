from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict, List
from app.models.resume import SectionType


class PersonalInfoBase(BaseModel):
    name: str
    email: Optional[str] = None
    telephone: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    is_visible: bool = True


class PersonalInfoCreate(PersonalInfoBase):
    pass


class PersonalInfoUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    is_visible: Optional[bool] = None


class PersonalInfo(PersonalInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


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
    personal_info: Optional[PersonalInfo] = None
    education: List[ResumeSection]
    experience: List[ResumeSection]
    skills: List[ResumeSection]
    projects: List[ResumeSection]