from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class BlogCategory(Base):
    __tablename__ = "blog_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    color = Column(String(7), default="#007bff")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    posts = relationship("BlogPost", back_populates="category")

    def __repr__(self):
        return f"<BlogCategory(id={self.id}, name='{self.name}')>"


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    summary = Column(Text)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("blog_categories.id"))
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    featured_image = Column(String(500))
    is_published = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))

    # 关系
    category = relationship("BlogCategory", back_populates="posts")
    author = relationship("User")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<BlogPost(id={self.id}, title='{self.title}')>"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("blog_posts.id"), nullable=False)
    author_name = Column(String(100), nullable=False)
    author_email = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=False, index=True)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    post = relationship("BlogPost", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, author='{self.author_name}')>"