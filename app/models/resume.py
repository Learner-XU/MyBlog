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


class PersonalInfo(Base):
    __tablename__ = "personal_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)
    telephone = Column(String(50), nullable=True)
    address = Column(String(500), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    github = Column(String(255), nullable=True)
    linkedin = Column(String(255), nullable=True)
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<PersonalInfo(id={self.id}, name='{self.name}')>"


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String(200), nullable=False)  # 学校名称
    degree = Column(String(100), nullable=False)       # 学历：本科、硕士、博士等
    major = Column(String(200), nullable=False)        # 专业
    start_date = Column(String(20), nullable=False)    # 开始日期 (YYYY-MM格式)
    end_date = Column(String(20), nullable=True)       # 结束日期 (YYYY-MM格式)，可为空表示在读
    gpa = Column(String(20), nullable=True)            # GPA成绩
    description = Column(Text, nullable=True)          # 描述信息
    order_index = Column(Integer, default=0, index=True)
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Education(id={self.id}, degree='{self.degree}', school_name='{self.school_name}')>"


class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(200), nullable=False)       # 公司名称
    position = Column(String(200), nullable=False)      # 职位
    start_date = Column(String(20), nullable=False)     # 开始日期 (YYYY-MM格式)
    end_date = Column(String(20), nullable=True)        # 结束日期 (YYYY-MM格式)，可为空表示在职
    description = Column(Text, nullable=True)           # 工作描述
    order_index = Column(Integer, default=0, index=True)
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Experience(id={self.id}, company='{self.company}', position='{self.position}')>"


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