# MyBlog - 开发快速参考

## 核心开发命令

### 环境与依赖
```bash
# 创建虚拟环境并激活
python -m venv venv
source venv/bin/activate

# 安装所有依赖
pip install -r requirements.txt

# 检查依赖树
pipdeptree
```

### 开发服务器
```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 指定工作进程数
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### 测试与质量
```bash
# 运行全部测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_blog.py -v

# 运行特定测试函数
pytest tests/test_blog.py::test_create_blog_post -v

# 测试覆盖率
pytest --cov=app --cov-report=html tests/

# 代码质量检查
black app/ tests/ --check
isort app/ tests/ --check-only
flake8 app/
mypy app/
```

### 数据库操作
```bash
# 数据库初始化（会删除现有数据）
python -m app.scripts.init_db

# 创建管理员用户
python -m app.scripts.create_admin

# 生成测试数据
python -m app.scripts.seed_data

# 数据库迁移检查
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(engine)"
```

### Docker 操作
```bash
# 启动所有服务
docker-compose up -d

# 停止服务
docker-compose down

# 重建并启动
docker-compose up -d --build

# 查看服务日志
docker-compose logs -f app

# 进入容器shell
docker-compose exec app bash
```

## 项目架构

### 核心架构模式
- **FastAPI应用层**: API路由处理、请求验证、响应格式化
- **业务逻辑层**: 数据库操作、业务规则实现
- **数据访问层**: SQLAlchemy ORM模型、数据库交互
- **工具层**: 工具函数、辅助功能

### 目录结构详解
```
app/
├── main.py              # FastAPI应用入口，路由注册
├── config.py           # Pydantic配置管理，环境变量加载
├── database.py         # SQLAlchemy引擎创建，会话管理
├── models/             # SQLAlchemy数据模型定义
│   ├── user.py         # 管理员用户模型
│   ├── blog.py         # 博客文章、分类、标签模型
│   ├── resume.py       # 简历章节模型
│   └── message.py      # 访客留言模型
├── schemas/            # Pydantic请求/响应模式
│   ├── auth.py         # 认证相关模式
│   ├── blog.py         # 博客相关模式
│   └── resume.py       # 简历相关模式
├── api/                # FastAPI路由模块
│   ├── auth.py         # 认证接口 (/api/auth/*)
│   ├── blog.py         # 博客接口 (/api/blog/*)
│   ├── resume.py       # 简历接口 (/api/resume/*)
│   └── admin.py        # 管理接口 (/api/admin/*)
├── core/               # 核心业务逻辑
│   ├── security.py     # JWT认证、密码哈希
│   ├── dependencies.py # FastAPI依赖注入
│   └── config.py       # 应用配置管理
├── utils/              # 工具函数库
│   ├── slug.py         # URL slug生成
│   └── time_utils.py   # 时间处理工具
└── scripts/            # 数据库管理脚本
    ├── init_db.py      # 数据库初始化
    ├── create_admin.py # 管理员创建
    └── seed_data.py    # 测试数据生成
```

### 关键模块依赖关系
- **main.py** → api模块 → core模块 → models/schemas
- **API路由** → 业务逻辑 → 数据模型
- **配置管理** → 贯穿所有层级

## 数据库设计

### 主要数据表
- **users**: 管理员用户表
- **blog_posts**: 博客文章表
- **blog_categories**: 文章分类表  
- **comments**: 评论表
- **resume_sections**: 简历章节表
- **messages**: 访客留言表

### 关键关系
- 文章与分类：多对一关系
- 文章与评论：一对多关系
- 简历按section_type分组管理

## API设计规范

### 认证机制
- 使用JWT Bearer Token认证
- 管理员操作需要认证头：`Authorization: Bearer <token>`
- Token有效期24小时

### 响应格式
```json
// 成功响应
{
  "data": {...},
  "message": "success"
}

// 错误响应
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": {...}
  }
}

// 分页响应
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

### 关键API端点
- `POST /api/auth/login`: 管理员登录
- `GET /api/blog/posts`: 获取文章列表（支持分页、搜索、分类筛选）
- `GET /api/blog/posts/{slug}`: 获取文章详情
- `GET /api/resume`: 获取完整简历数据
- `POST /api/comments`: 提交评论（需审核）

## 开发规范

### 代码风格
- 使用Black进行代码格式化
- 使用isort管理import顺序
- 遵循PEP 8规范
- 使用类型注解

### 数据验证
- 所有API输入使用Pydantic模式验证
- 数据库模型使用SQLAlchemy定义
- 敏感数据（如密码）必须哈希存储

### 错误处理
- 使用FastAPI的HTTPException处理HTTP错误
- 数据库操作需要异常处理
- 记录详细的错误日志

### 安全考虑
- 所有用户输入必须验证和过滤
- 防止SQL注入（使用SQLAlchemy ORM）
- 防止XSS攻击（HTML内容过滤）
- API限流防止暴力攻击

## 测试策略

### 测试类型
- **单元测试**: 测试单个函数/方法
- **集成测试**: 测试API端点
- **数据库测试**: 使用测试数据库

### 测试命令
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_blog.py

# 生成覆盖率报告
pytest --cov=app tests/

# 测试特定功能
pytest -k "test_blog" -v
```

## 部署说明

### 环境变量配置 (.env文件)
```bash
# 数据库配置
DATABASE_URL=mysql://user:password@localhost:3306/myblog

# 应用配置
SECRET_KEY=your-secure-jwt-secret-key
DEBUG=true

# Redis配置（缓存，可选）
REDIS_URL=redis://localhost:6379

# CORS配置
FRONTEND_URL=http://localhost:3000

# 管理员初始账户
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_EMAIL=admin@example.com
```

## 常见问题

### 数据库连接问题
- 检查MySQL服务是否启动
- 确认数据库连接字符串正确
- 检查数据库用户权限

### 认证问题
- JWT Token过期需要重新登录
- 确认SECRET_KEY配置正确
- 检查Token格式是否正确

### 性能优化
- 使用数据库索引优化查询
- 实现Redis缓存热点数据
- 使用pagination避免大数据量查询

## 扩展功能建议

### 可选功能
- 文章标签系统
- 全文搜索（Elasticsearch）
- 图片上传和管理
- 社交媒体集成
- RSS订阅功能
- 访问统计分析
- 邮件订阅通知