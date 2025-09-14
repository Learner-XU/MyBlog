from .auth import router as auth_router
from .blog import router as blog_router
from .resume import router as resume_router
from .admin import router as admin_router

__all__ = ["auth_router", "blog_router", "resume_router", "admin_router"]