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


class EducationBase(BaseModel):
    degree: str
    major: str
    school_name: str
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    description: Optional[str] = None
    order_index: int = 0
    is_visible: bool = True


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    degree: Optional[str] = None
    major: Optional[str] = None
    school: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    is_visible: Optional[bool] = None


class Education(EducationBase):
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


class ExperienceBase(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None
    order_index: int = 0
    is_visible: bool = True


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    is_visible: Optional[bool] = None


class Experience(ExperienceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeSection(ResumeSectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeData(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    education: List[Education]
    experience: List[Experience]
    skills: List[ResumeSection]
    projects: List[ResumeSection]