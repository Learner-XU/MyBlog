from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.security import get_current_active_user
from app.models.resume import ResumeSection, SectionType
from app.schemas.resume import (
    ResumeSection as ResumeSectionSchema, 
    ResumeSectionCreate, ResumeSectionUpdate, 
    ResumeData
)

router = APIRouter(prefix="/api/resume", tags=["简历"])


@router.get("", response_model=ResumeData)
def read_resume(db: Session = Depends(get_db)):
    """获取完整简历信息"""
    sections = db.query(ResumeSection)\
                .filter(ResumeSection.is_visible == True)\
                .order_by(ResumeSection.order_index)\
                .all()
    
    # 按类型分组
    resume_data = {
        "personal_info": [],
        "education": [],
        "experience": [],
        "skills": [],
        "projects": []
    }
    
    for section in sections:
        resume_data[section.section_type.value].append(section)
    
    return ResumeData(**resume_data)


@router.get("/sections", response_model=List[ResumeSectionSchema])
def read_resume_sections(
    section_type: SectionType = None, 
    db: Session = Depends(get_db)
):
    """获取简历章节列表，支持按类型筛选"""
    query = db.query(ResumeSection)
    
    if section_type:
        query = query.filter(ResumeSection.section_type == section_type)
    
    sections = query.order_by(ResumeSection.order_index).all()
    return sections


@router.post("/sections", response_model=ResumeSectionSchema)
def create_resume_section(
    section: ResumeSectionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """创建新的简历章节"""
    db_section = ResumeSection(**section.model_dump())
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    
    return db_section


@router.put("/sections/{section_id}", response_model=ResumeSectionSchema)
def update_resume_section(
    section_id: int,
    section_update: ResumeSectionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """更新简历章节"""
    db_section = db.query(ResumeSection).filter(ResumeSection.id == section_id).first()
    if not db_section:
        raise HTTPException(status_code=404, detail="章节未找到")
    
    for key, value in section_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_section, key, value)
    
    db.commit()
    db.refresh(db_section)
    
    return db_section


@router.delete("/sections/{section_id}")
def delete_resume_section(
    section_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """删除简历章节"""
    db_section = db.query(ResumeSection).filter(ResumeSection.id == section_id).first()
    if not db_section:
        raise HTTPException(status_code=404, detail="章节未找到")
    
    db.delete(db_section)
    db.commit()
    
    return {"message": "章节删除成功"}