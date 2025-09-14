from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class BlogCategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    color: str = "#007bff"


class BlogCategoryCreate(BlogCategoryBase):
    pass


class BlogCategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


class BlogCategory(BlogCategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BlogPostBase(BaseModel):
    title: str
    slug: Optional[str] = None
    summary: Optional[str] = None
    content: str
    category_id: Optional[int] = None
    featured_image: Optional[str] = None
    is_published: bool = False


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    featured_image: Optional[str] = None
    is_published: Optional[bool] = None


class BlogPostList(BaseModel):
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    category: Optional[BlogCategory] = None
    view_count: int
    is_published: bool
    created_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BlogPost(BlogPostList):
    content: str
    author_id: int
    featured_image: Optional[str] = None
    updated_at: datetime


class CommentBase(BaseModel):
    post_id: int
    author_name: str = Field(..., max_length=100)
    author_email: str = Field(..., max_length=100)
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BlogPostWithComments(BlogPost):
    comments: List[Comment] = []


class PaginatedResponse(BaseModel):
    items: List[BlogPostList]
    total: int
    page: int
    size: int
    pages: int