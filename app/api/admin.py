from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Dict, List
from app.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.blog import Comment, BlogPost
from app.models.message import Message
from app.schemas.blog import Comment as CommentSchema
from app.schemas.message import Message as MessageSchema

router = APIRouter(prefix="/api/admin", tags=["管理"])


@router.get("/dashboard")
def get_admin_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """获取管理后台仪表板数据"""
    # 统计信息
    total_posts = db.query(BlogPost).count()
    total_comments = db.query(Comment).count()
    total_messages = db.query(Message).count()
    total_views = db.query(func.sum(BlogPost.view_count)).scalar() or 0
    
    # 近期评论（未审批的）
    recent_comments = db.query(Comment)\
                        .filter(Comment.is_approved == False)\
                        .order_by(desc(Comment.created_at))\
                        .limit(10)\
                        .all()
    
    # 近期留言（未阅读的）
    recent_messages = db.query(Message)\
                       .filter(Message.is_read == False)\
                       .order_by(desc(Message.created_at))\
                       .limit(10)\
                       .all()
    
    # 最近7天的访问统计
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_posts = db.query(BlogPost)\
                    .filter(BlogPost.published_at >= seven_days_ago)\
                    .order_by(desc(BlogPost.view_count))\
                    .limit(5)\
                    .all()
    
    return {
        "stats": {
            "total_posts": total_posts,
            "total_comments": total_comments,
            "total_messages": total_messages,
            "total_views": total_views
        },
        "recent_comments": recent_comments,
        "recent_messages": recent_messages,
        "recent_posts": recent_posts
    }


@router.get("/comments/pending", response_model=List[CommentSchema])
def get_pending_comments(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """获取待审批的评论列表"""
    comments = db.query(Comment)\
                .filter(Comment.is_approved == False)\
                .order_by(desc(Comment.created_at))\
                .all()
    return comments


@router.post("/comments/{comment_id}/approve")
def approve_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """审批通过评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="评论未找到")
    
    comment.is_approved = True
    db.commit()
    
    return {"message": "评论已审批通过"}


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """删除评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="评论未找到")
    
    db.delete(comment)
    db.commit()
    
    return {"message": "评论删除成功"}


@router.get("/messages", response_model=List[MessageSchema])
def get_messages(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """获取留言列表"""
    messages = db.query(Message).order_by(desc(Message.created_at)).all()
    return messages


@router.get("/messages/{message_id}", response_model=MessageSchema)
def get_message(message_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """获取留言详情"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="留言未找到")
    
    # 标记为已读
    if not message.is_read:
        message.is_read = True
        db.commit()
        db.refresh(message)
    
    return message


@router.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """删除留言"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="留言未找到")
    
    db.delete(message)
    db.commit()
    
    return {"message": "留言删除成功"}


@router.get("/users", response_model=List[dict])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """获取用户列表"""
    users = db.query(User).order_by(User.created_at).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
        for user in users
    ]


@router.post("/users/{user_id}/toggle-active")
def toggle_user_active(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """切换用户启用状态"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能禁用当前用户")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    
    user.is_active = not user.is_active
    db.commit()
    
    status = "启用" if user.is_active else "禁用"
    return {"message": f"用户 {status} 成功"}