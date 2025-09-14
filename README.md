# MyBlog - 个人简历与博客网站

基于Python FastAPI + MySQL构建的现代化个人简历与博客展示网站。

## ✨ 功能特性

- 🏠 **个人简历展示** - 动态配置的简历章节，支持个人信息、教育经历、工作经验等
- 📝 **博客系统** - 文章发布、分类管理、评论系统
- 💬 **评论互动** - 访客评论功能，支持管理员审核
- 📧 **留言板** - 访客留言功能
- 🔐 **后台管理** - 安全的管理员认证，内容管理界面
- 🚀 **高性能** - 基于FastAPI的高性能异步框架
- 🐳 **容器化** - 支持Docker部署

## 🛠️ 技术栈

- **后端框架**: FastAPI
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy
- **认证**: JWT Token
- **部署**: Docker + Docker Compose

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MySQL 8.0+
- Docker & Docker Compose (可选)

### 本地开发

1. **克隆项目**
```bash
git clone <repository-url>
cd MyBlog
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

5. **初始化数据库**
```bash
python -m app.scripts.init_db
python -m app.scripts.create_admin
```

6. **启动开发服务器**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000 查看应用，http://localhost:8000/docs 查看API文档。

### Docker部署

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f app
```

## 📖 项目文档

- [项目概要设计](./项目概要设计.md) - 项目整体架构和设计思路
- [详细设计文档](./详细设计文档.md) - 数据库设计、API设计等详细说明
- [开发指南](./CODEBUDDY.md) - 开发环境配置和编码规范

## 🏗️ 项目结构

```
MyBlog/
├── app/                    # 应用主目录
│   ├── main.py            # FastAPI应用入口
│   ├── config.py          # 配置文件
│   ├── database.py        # 数据库连接
│   ├── models/            # 数据模型
│   ├── schemas/           # Pydantic模式
│   ├── api/               # API路由
│   ├── core/              # 核心功能
│   ├── utils/             # 工具函数
│   └── scripts/           # 数据库脚本
├── tests/                 # 测试文件
├── docker-compose.yml     # Docker配置
├── requirements.txt       # Python依赖
└── README.md             # 项目说明
```

## 🔧 开发命令

```bash
# 运行测试
pytest tests/ -v

# 代码格式化
black app/ tests/
isort app/ tests/

# 代码检查
flake8 app/
mypy app/

# 创建管理员
python -m app.scripts.create_admin

# 初始化测试数据
python -m app.scripts.seed_data
```

## 📊 API文档

启动服务后访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

主要API端点：

- `POST /api/auth/login` - 管理员登录
- `GET /api/resume` - 获取简历信息
- `GET /api/blog/posts` - 获取博客文章列表
- `GET /api/blog/posts/{slug}` - 获取文章详情
- `POST /api/comments` - 提交评论

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- 邮箱: your-email@example.com
- 项目Issues: [GitHub Issues](https://github.com/your-username/MyBlog/issues)