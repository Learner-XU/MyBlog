import express from 'express';
import cors from 'cors';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const app = express();
const PORT = 8000;
const JWT_SECRET = 'your-secret-key-change-in-production';

// 中间件
app.use(cors());
app.use(express.json());

// 模拟数据
const users = [
  {
    id: 1,
    username: 'admin',
    email: 'admin@example.com',
    full_name: 'Administrator',
    password_hash: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password: admin123
    is_active: true,
    created_at: '2024-01-01T00:00:00'
  }
];

const blogPosts = [
  {
    id: 1,
    title: '欢迎来到MyBlog',
    slug: 'welcome-to-myblog',
    summary: '这是我的第一篇博客文章，欢迎来到我的个人博客网站！',
    content: '这是我的第一篇博客文章。我将在这里分享技术知识、生活感悟和个人项目。\n\n## 技术栈\n- 前端: React + TypeScript\n- 后端: FastAPI (Node.js模拟)\n- 数据库: MySQL (内存模拟)\n\n期待与大家分享更多内容！',
    category_id: 1,
    author_id: 1,
    featured_image: null,
    is_published: true,
    view_count: 42,
    created_at: '2024-01-01T10:00:00',
    updated_at: '2024-01-01T10:00:00',
    published_at: '2024-01-01T10:00:00'
  },
  {
    id: 2,
    title: 'React开发最佳实践',
    slug: 'react-best-practices',
    summary: '分享一些React开发中的最佳实践和经验',
    content: '在React开发中，遵循一些最佳实践可以大大提高代码质量和开发效率。\n\n## 组件设计\n- 保持组件单一职责\n- 使用TypeScript增强类型安全\n- 合理使用Hook\n\n## 状态管理\n- 使用Context API管理全局状态\n- 合理使用useState和useReducer',
    category_id: 1,
    author_id: 1,
    featured_image: null,
    is_published: true,
    view_count: 28,
    created_at: '2024-01-02T14:30:00',
    updated_at: '2024-01-02T14:30:00',
    published_at: '2024-01-02T14:30:00'
  }
];

const blogCategories = [
  { id: 1, name: '技术文章', slug: 'technology', description: '技术相关的文章', color: '#007bff', created_at: '2024-01-01T00:00:00' },
  { id: 2, name: '生活随笔', slug: 'life', description: '生活感悟和随笔', color: '#28a745', created_at: '2024-01-01T00:00:00' }
];

const resumeSections = {
  personal_info: [
    {
      id: 1,
      section_type: 'personal_info',
      title: '个人信息',
      content: '姓名：张三\\n邮箱：zhangsan@example.com\\n电话：138-****-****\\n地址：北京市朝阳区',
      order_index: 1,
      is_visible: true,
      created_at: '2024-01-01T00:00:00',
      updated_at: '2024-01-01T00:00:00'
    }
  ],
  education: [
    {
      id: 2,
      section_type: 'education',
      title: '教育背景',
      content: '2015-2019 北京大学 计算机科学与技术 本科\\n2019-2022 清华大学 软件工程 硕士',
      order_index: 2,
      is_visible: true,
      created_at: '2024-01-01T00:00:00',
      updated_at: '2024-01-01T00:00:00'
    }
  ],
  experience: [
    {
      id: 3,
      section_type: 'experience',
      title: '工作经历',
      content: '2022-至今 某某科技公司 高级软件工程师\\n2020-2022 某某互联网公司 后端开发工程师',
      order_index: 3,
      is_visible: true,
      created_at: '2024-01-01T00:00:00',
      updated_at: '2024-01-01T00:00:00'
    }
  ],
  skills: [
    {
      id: 4,
      section_type: 'skills',
      title: '技术技能',
      content: 'Python, FastAPI, Django\\nMySQL, Redis, MongoDB\\nDocker, Kubernetes, AWS',
      order_index: 4,
      is_visible: true,
      created_at: '2024-01-01T00:00:00',
      updated_at: '2024-01-01T00:00:00'
    }
  ],
  projects: [
    {
      id: 5,
      section_type: 'projects',
      title: '项目经验',
      content: '1. 电商平台后端开发\\n2. 微服务架构设计\\n3. 自动化部署系统',
      order_index: 5,
      is_visible: true,
      created_at: '2024-01-01T00:00:00',
      updated_at: '2024-01-01T00:00:00'
    }
  ]
};

// 认证中间件
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: '无法验证凭据' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = users.find(u => u.username === decoded.sub);
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Token无效' });
  }
};

// 路由

// 健康检查
app.get('/', (req, res) => {
  res.json({ 
    message: '欢迎使用MyBlog API',
    version: '1.0.0',
    docs: '/docs'
  });
});

// 认证路由
app.post('/api/auth/login', async (req, res) => {
  const { username, password } = req.body;

  const user = users.find(u => u.username === username);
  if (!user || !(await bcrypt.compare(password, user.password_hash))) {
    return res.status(401).json({ error: '用户名或密码错误' });
  }

  if (!user.is_active) {
    return res.status(400).json({ error: '用户已禁用' });
  }

  const token = jwt.sign({ sub: user.username }, JWT_SECRET, { expiresIn: '24h' });

  res.json({
    access_token: token,
    token_type: 'bearer',
    user: {
      id: user.id,
      username: user.username,
      full_name: user.full_name
    }
  });
});

app.get('/api/auth/me', authenticateToken, (req, res) => {
  res.json(req.user);
});

// 博客路由
app.get('/api/blog/posts', (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const size = parseInt(req.query.size) || 10;
  const categoryId = req.query.category ? parseInt(req.query.category) : null;
  const search = req.query.search || '';

  let filteredPosts = blogPosts.filter(post => post.is_published);

  if (categoryId) {
    filteredPosts = filteredPosts.filter(post => post.category_id === categoryId);
  }

  if (search) {
    filteredPosts = filteredPosts.filter(post => 
      post.title.toLowerCase().includes(search.toLowerCase()) ||
      (post.summary && post.summary.toLowerCase().includes(search.toLowerCase()))
    );
  }

  const startIndex = (page - 1) * size;
  const endIndex = startIndex + size;
  const paginatedPosts = filteredPosts.slice(startIndex, endIndex);

  res.json({
    items: paginatedPosts.map(post => ({
      ...post,
      category: blogCategories.find(c => c.id === post.category_id)
    })),
    total: filteredPosts.length,
    page,
    size,
    pages: Math.ceil(filteredPosts.length / size)
  });
});

app.get('/api/blog/posts/:slug', (req, res) => {
  const post = blogPosts.find(p => p.slug === req.params.slug && p.is_published);
  if (!post) {
    return res.status(404).json({ error: '文章未找到' });
  }

  // 增加访问计数
  post.view_count++;

  res.json({
    ...post,
    category: blogCategories.find(c => c.id === post.category_id),
    comments: []
  });
});

app.get('/api/blog/categories', (req, res) => {
  res.json(blogCategories);
});

// 简历路由
app.get('/api/resume', (req, res) => {
  res.json(resumeSections);
});

app.get('/api/resume/sections', (req, res) => {
  const sectionType = req.query.section_type;
  if (sectionType && resumeSections[sectionType]) {
    res.json(resumeSections[sectionType]);
  } else {
    const allSections = Object.values(resumeSections).flat();
    res.json(allSections);
  }
});

// 管理路由（需要认证）
app.get('/api/admin/dashboard', authenticateToken, (req, res) => {
  res.json({
    stats: {
      total_posts: blogPosts.length,
      total_comments: 0,
      total_messages: 0,
      total_views: blogPosts.reduce((sum, post) => sum + post.view_count, 0)
    },
    recent_comments: [],
    recent_messages: []
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`🚀 MyBlog模拟服务器运行在 http://localhost:${PORT}`);
  console.log(`📚 API文档: http://localhost:${PORT}/`);
  console.log(`🔑 默认管理员: admin / admin123`);
});