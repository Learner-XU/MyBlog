from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api import auth_router, blog_router, resume_router, admin_router

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="个人简历与博客网站API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册API路由
app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(resume_router)
app.include_router(admin_router)


@app.get("/")
async def root():
    return {
        "message": "欢迎使用MyBlog API",
        "version": settings.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)