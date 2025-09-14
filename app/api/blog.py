from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.core.dependencies import get_pagination_params, get_current_admin_user
from app.core.security import get_current_active_user
from app.models.blog import BlogPost, BlogCategory, Comment
from app.models.user import User
from app.schemas.blog import (
    BlogPost as BlogPostSchema, BlogPostList, BlogPostCreate, BlogPostUpdate,
    BlogCategory as BlogCategorySchema, BlogCategoryCreate, BlogCategoryUpdate,
    Comment as CommentSchema, CommentCreate, PaginatedResponse, BlogPostWithComments
)
from app.schemas.user import User as UserSchema
from app.utils.helpers import slugify

router = APIRouter(prefix="/api/blog", tags=["博客"])


# 博客文章相关路由

@router.get("/posts", response_model=PaginatedResponse)
def read_blog_posts(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    category: Optional[int] = Query(None, description="分类ID"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    published_only: bool = Query(True, description="是否只显示已发布文章")
):
    """获取博客文章列表"""
    query = db.query(BlogPost)
    
    if published_only:
        query = query.filter(BlogPost.is_published == True)
    
    if category:
        query = query.filter(BlogPost.category_id == category)
    
    if search:
        query = query.filter(BlogPost.title.ilike(f"%{search}%"))
    
    total = query.count()
    posts = query.order_by(BlogPost.published_at.desc(), BlogPost.created_at.desc())\
                .offset(pagination["offset"])\
                .limit(pagination["size"])\
                .all()
    
    pages = (total + pagination["size"] - 1) // pagination["size"]
    
    return {
        "items": posts,
        "total": total,
        "page": pagination["page"],
        "size": pagination["size"],
        "pages": pages
    }


@router.get("/posts/{slug}", response_model=BlogPostWithComments)
def read_blog_post(slug: str, db: Session = Depends(get_db)):
    """获取博客文章详情"""
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post or not post.is_published:
        raise HTTPException(status_code=404, detail="文章未找到")
    
    # 增加访问计数
    post.view_count += 1
    db.commit()
    db.refresh(post)
    
    # 获取已批准的评论
    approved_comments = db.query(Comment).filter(
        Comment.post_id == post.id, Comment.is_approved == True
    ).order_by(Comment.created_at.desc()).all()
    
    return BlogPostWithComments(
        **post.__dict__,
        comments=approved_comments
    )


@router.post("/posts", response_model=BlogPostSchema)
def create_blog_post(
    post: BlogPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """创建新的博客文章"""
    if not post.slug:
        post.slug = slugify(post.title)
    
    # 检查slug是否已存在
    existing_post = db.query(BlogPost).filter(BlogPost.slug == post.slug).first()
    if existing_post:
        post.slug = f"{post.slug}-{int(db.query(BlogPost).count()) + 1}"
    
    db_post = BlogPost(
        **post.model_dump(),
        author_id=current_user.id
    )
    
    if post.is_published:
        db_post.published_at = db_post.created_at
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post


@router.put("/posts/{post_id}", response_model=BlogPostSchema)
def update_blog_post(
    post_id: int,
    post_update: BlogPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """更新博客文章"""
    db_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="文章未找到")
    
    for key, value in post_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_post, key, value)
    
    # 如果从未发布到发布，设置发布时间
    if not db_post.is_published and post_update.is_published:
        db_post.published_at = db_post.updated_at
    
    db.commit()
    db.refresh(db_post)
    
    return db_post


@router.delete("/posts/{post_id}")
def delete_blog_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """删除博客文章"""
    db_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="文章未找到")
    
    db.delete(db_post)
    db.commit()
    
    return {"message": "文章删除成功"}


# 评论相关路由

@router.post("/comments", response_model=CommentSchema)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    """创建新的评论"""
    # 检查文章是否存在
    post = db.query(BlogPost).filter(BlogPost.id == comment.post_id).first()
    if not post or not post.is_published:
        raise HTTPException(status_code=404, detail="文章未找到")
    
    db_comment = Comment(**comment.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return db_comment


@router.get("/posts/{post_id}/comments", response_model=list[CommentSchema])
def read_post_comments(post_id: int, db: Session = Depends(get_db)):
    """获取文章评论列表"""
    # 只返回已批准的评论
    comments = db.query(Comment).filter(
        Comment.post_id == post_id, Comment.is_approved == True
    ).order_by(Comment.created_at.desc()).all()
    
    return comments


# 分类相关路由

@router.get("/categories", response_model=list[BlogCategorySchema])
def read_categories(db: Session = Depends(get_db)):
    """获取博客分类列表"""
    categories = db.query(BlogCategory).order_by(BlogCategory.name).all()
    return categories


@router.post("/categories", response_model=BlogCategorySchema)
def create_category(
    category: BlogCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """创建新的博客分类"""
    db_category = BlogCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.put("/categories/{category_id}", response_model=BlogCategorySchema)
def update_category(
    category_id: int,
    category_update: BlogCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """更新博客分类"""
    db_category = db.query(BlogCategory).filter(BlogCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="分类未找到")
    
    for key, value in category_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """删除博客分类"""
    db_category = db.query(BlogCategory).filter(BlogCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="分类未找到")
    
    # 检查分类下是否有文章
    post_count = db.query(BlogPost).filter(BlogPost.category_id == category_id).count()
    if post_count > 0:
        raise HTTPException(
            status_code=400, 
            detail="该分类下还有文章，无法删除"
        )
    
    db.delete(db_category)
    db.commit()
    
    return {"message": "分类删除成功"}