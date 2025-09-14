from typing import Optional
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.config import settings


def get_pagination_params(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size, description="每页数量")
):
    """获取分页参数"""
    return {"page": page, "size": size, "offset": (page - 1) * size}


def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """获取当前管理员用户"""
    # 这里可以添加管理员权限检查逻辑
    # 例如：if not current_user.is_admin: raise HTTPException(...)
    return current_user


def get_optional_user(
    token: Optional[str] = Query(None), 
    db: Session = Depends(get_db)
):
    """获取可选用户（用于某些可选的认证功能）"""
    if token:
        try:
            return get_current_active_user(token, db)
        except HTTPException:
            return None
    return None