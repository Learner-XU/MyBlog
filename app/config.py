from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 应用配置
    app_name: str = "MyBlog"
    debug: bool = False
    version: str = "1.0.0"
    
    # 数据库配置
    database_url: str = "mysql+pymysql://root:password@localhost:3306/myblog"
    
    # 安全配置
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24小时
    
    # Redis配置（可选）
    redis_url: Optional[str] = None
    
    # 邮件配置（可选）
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_tls: bool = True
    
    # 文件上传配置
    upload_dir: str = "static/uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = ["jpg", "jpeg", "png", "gif", "webp"]
    
    # 分页配置
    default_page_size: int = 10
    max_page_size: int = 100
    
    # 缓存配置
    cache_expire_time: int = 60 * 30  # 30分钟
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局配置实例
settings = Settings()