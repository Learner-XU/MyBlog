#!/usr/bin/env python3
"""
简易FastAPI服务器启动脚本
由于环境限制，使用系统Python直接运行
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def install_missing_dependencies():
    """尝试安装缺失的依赖"""
    missing_modules = []
    
    # 检查核心依赖
    dependencies = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('sqlalchemy', 'sqlalchemy'),
        ('pymysql', 'pymysql'),
        ('jose', 'python-jose'),
        ('passlib', 'passlib'),
        ('pydantic', 'pydantic'),
    ]
    
    for import_name, package_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {package_name} 已安装")
        except ImportError:
            print(f"❌ {package_name} 未安装")
            missing_modules.append(package_name)
    
    return missing_modules

def start_minimal_server():
    """启动一个最小化的FastAPI服务器"""
    print("🚀 启动最小化FastAPI服务器...")
    
    # 创建简易的FastAPI应用
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(title="MyBlog API", version="1.0.0")
    
    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 添加基本路由
    @app.get("/")
    async def root():
        return {
            "message": "MyBlog API 正在运行",
            "version": "1.0.0",
            "status": "minimal_mode"
        }
    
    @app.get("/api/health")
    async def health_check():
        return {"status": "healthy"}
    
    @app.get("/api/blog/posts")
    async def get_blog_posts():
        # 返回模拟数据
        return {
            "items": [
                {
                    "id": 1,
                    "title": "欢迎来到MyBlog",
                    "slug": "welcome-to-myblog",
                    "summary": "这是我的第一篇博客文章",
                    "view_count": 42,
                    "created_at": "2024-01-01T00:00:00"
                }
            ],
            "total": 1,
            "page": 1,
            "size": 10,
            "pages": 1
        }
    
    @app.get("/api/resume")
    async def get_resume():
        # 返回模拟简历数据
        return {
            "personal_info": [
                {
                    "title": "个人信息",
                    "content": "姓名：张三\\n邮箱：example@email.com"
                }
            ],
            "education": [
                {
                    "title": "教育背景", 
                    "content": "2015-2019 北京大学 计算机科学与技术"
                }
            ]
        }
    
    # 启动服务器
    import uvicorn
    print("🌐 服务器启动成功！")
    print("📍 访问地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("🔑 前端地址: http://localhost:3000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    print("=" * 50)
    print("MyBlog 服务器启动器")
    print("=" * 50)
    
    # 检查依赖
    missing = install_missing_dependencies()
    
    if missing:
        print(f"\n⚠️  缺少 {len(missing)} 个依赖包")
        print("💡 建议在有网络的环境中使用: pip install -r requirements.txt")
        print("🚀 正在启动最小化模式...")
    
    try:
        start_minimal_server()
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请检查Python环境或联系管理员")