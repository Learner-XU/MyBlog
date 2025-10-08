from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.core.security import get_current_active_user
from app.models.resume import ResumeSection, SectionType, PersonalInfo, Education, Experience
from app.schemas.resume import (
    ResumeSection as ResumeSectionSchema, 
    ResumeSectionCreate, ResumeSectionUpdate, 
    ResumeData,
    PersonalInfo as PersonalInfoSchema,
    PersonalInfoCreate, PersonalInfoUpdate,
    Education as EducationSchema,
    EducationCreate, EducationUpdate,
    Experience as ExperienceSchema,
    ExperienceCreate, ExperienceUpdate
)

router = APIRouter(prefix="/api/resume", tags=["简历"])


@router.get("", response_model=ResumeData)
def read_resume(db: Session = Depends(get_db)):
    """获取完整简历信息"""
    try:
        # 获取个人信息
        personal_info = db.query(PersonalInfo)\
                         .filter(PersonalInfo.is_visible == True)\
                         .first()
        
        # 获取教育背景
        education = db.query(Education)\
                     .filter(Education.is_visible == True)\
                     .order_by(Education.order_index)\
                     .all()
        
        # 获取工作经历
        experience = db.query(Experience)\
                      .filter(Experience.is_visible == True)\
                      .order_by(Experience.order_index)\
                      .all()
        
        # 获取技能章节
        skills = db.query(ResumeSection)\
                  .filter(ResumeSection.is_visible == True)\
                  .filter(ResumeSection.section_type == SectionType.skills)\
                  .order_by(ResumeSection.order_index)\
                  .all()
        
        # 获取项目章节
        projects = db.query(ResumeSection)\
                    .filter(ResumeSection.is_visible == True)\
                    .filter(ResumeSection.section_type == SectionType.projects)\
                    .order_by(ResumeSection.order_index)\
                    .all()
        
        # 按类型分组
        resume_data = {
            "personal_info": personal_info,
            "education": education,
            "experience": experience,
            "skills": skills,
            "projects": projects
        }
        return resume_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


# 个人信息相关API
@router.get("/personal-info", response_model=PersonalInfoSchema)
def read_personal_info(db: Session = Depends(get_db)):
    """获取个人信息"""
    personal_info = db.query(PersonalInfo)\
                     .filter(PersonalInfo.is_visible == True)\
                     .first()
    
    if not personal_info:
        raise HTTPException(status_code=404, detail="个人信息未找到")
    
    return personal_info


@router.post("/personal-info", response_model=PersonalInfoSchema)
def create_personal_info(
    personal_info: PersonalInfoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """创建个人信息"""
    # 检查是否已存在个人信息
    existing_info = db.query(PersonalInfo).first()
    if existing_info:
        raise HTTPException(status_code=400, detail="个人信息已存在，请使用更新接口")
    
    db_personal_info = PersonalInfo(**personal_info.model_dump())
    db.add(db_personal_info)
    db.commit()
    db.refresh(db_personal_info)
    
    return db_personal_info


@router.put("/personal-info", response_model=PersonalInfoSchema)
def update_personal_info(
    personal_info_update: PersonalInfoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """更新个人信息"""
    db_personal_info = db.query(PersonalInfo).first()
    if not db_personal_info:
        raise HTTPException(status_code=404, detail="个人信息未找到")
    
    for key, value in personal_info_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_personal_info, key, value)
    
    db.commit()
    db.refresh(db_personal_info)
    
    return db_personal_info


@router.delete("/personal-info")
def delete_personal_info(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """删除个人信息"""
    db_personal_info = db.query(PersonalInfo).first()
    if not db_personal_info:
        raise HTTPException(status_code=404, detail="个人信息未找到")
    
    db.delete(db_personal_info)
    db.commit()
    
    return {"message": "个人信息删除成功"}


# 教育背景相关API
@router.get("/education", response_model=List[EducationSchema])
def read_education(db: Session = Depends(get_db)):
    """获取所有教育背景"""
    return db.query(Education)\
             .filter(Education.is_visible == True)\
             .order_by(Education.order_index)\
             .all()


@router.post("/education", response_model=EducationSchema)
def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """创建教育背景"""
    db_education = Education(**education.model_dump())
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education


@router.get("/education/{education_id}", response_model=EducationSchema)
def read_education_by_id(education_id: int, db: Session = Depends(get_db)):
    """根据ID获取教育背景"""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if not db_education:
        raise HTTPException(status_code=404, detail="教育背景未找到")
    return db_education


@router.put("/education/{education_id}", response_model=EducationSchema)
def update_education(
    education_id: int,
    education_update: EducationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """更新教育背景"""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if not db_education:
        raise HTTPException(status_code=404, detail="教育背景未找到")
    
    # 更新字段
    for key, value in education_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_education, key, value)
    
    db.commit()
    db.refresh(db_education)
    
    return db_education


@router.delete("/education/{education_id}")
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """删除教育背景"""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if not db_education:
        raise HTTPException(status_code=404, detail="教育背景未找到")
    
    db.delete(db_education)
    db.commit()
    
    return {"message": "教育背景删除成功"}


# 工作经历相关API
@router.get("/experience", response_model=List[ExperienceSchema])
def read_experience(db: Session = Depends(get_db)):
    """获取所有工作经历"""
    return db.query(Experience)\
             .filter(Experience.is_visible == True)\
             .order_by(Experience.order_index)\
             .all()


@router.post("/experience", response_model=ExperienceSchema)
def create_experience(
    experience: ExperienceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """创建工作经历"""
    db_experience = Experience(**experience.model_dump())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.get("/experience/{experience_id}", response_model=ExperienceSchema)
def read_experience_by_id(experience_id: int, db: Session = Depends(get_db)):
    """根据ID获取工作经历"""
    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="工作经历未找到")
    return db_experience


@router.put("/experience/{experience_id}", response_model=ExperienceSchema)
def update_experience(
    experience_id: int,
    experience_update: ExperienceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """更新工作经历"""
    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="工作经历未找到")
    
    # 更新字段
    for key, value in experience_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_experience, key, value)
    
    db.commit()
    db.refresh(db_experience)
    
    return db_experience


@router.delete("/experience/{experience_id}")
def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """删除工作经历"""
    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="工作经历未找到")
    
    db.delete(db_experience)
    db.commit()
    
    return {"message": "工作经历删除成功"}