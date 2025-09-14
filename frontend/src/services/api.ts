import axios from 'axios';
import type { 
  User, UserLogin, Token, 
  BlogPost, BlogPostList, BlogPostCreate, BlogCategory,
  Comment, CommentCreate, ResumeData, ResumeSection,
  Message, PaginatedResponse 
} from '../types';

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // token过期，清除本地存储
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 认证相关API
export const authApi = {
  login: (credentials: UserLogin): Promise<{ data: Token }> =>
    api.post('/auth/login', credentials),

  loginJson: (credentials: UserLogin): Promise<{ data: Token }> =>
    api.post('/auth/login/json', credentials),

  getMe: (): Promise<{ data: User }> =>
    api.get('/auth/me'),
};

// 博客相关API
export const blogApi = {
  getPosts: (params?: {
    page?: number;
    size?: number;
    category?: number;
    search?: string;
    published_only?: boolean;
  }): Promise<{ data: PaginatedResponse<BlogPostList> }> =>
    api.get('/blog/posts', { params }),

  getPost: (slug: string): Promise<{ data: BlogPost }> =>
    api.get(`/blog/posts/${slug}`),

  createPost: (post: BlogPostCreate): Promise<{ data: BlogPost }> =>
    api.post('/blog/posts', post),

  updatePost: (id: number, post: Partial<BlogPostCreate>): Promise<{ data: BlogPost }> =>
    api.put(`/blog/posts/${id}`, post),

  deletePost: (id: number): Promise<void> =>
    api.delete(`/blog/posts/${id}`),

  getCategories: (): Promise<{ data: BlogCategory[] }> =>
    api.get('/blog/categories'),

  createCategory: (category: Partial<BlogCategory>): Promise<{ data: BlogCategory }> =>
    api.post('/blog/categories', category),

  updateCategory: (id: number, category: Partial<BlogCategory>): Promise<{ data: BlogCategory }> =>
    api.put(`/blog/categories/${id}`, category),

  deleteCategory: (id: number): Promise<void> =>
    api.delete(`/blog/categories/${id}`),

  createComment: (comment: CommentCreate): Promise<{ data: Comment }> =>
    api.post('/blog/comments', comment),

  getPostComments: (postId: number): Promise<{ data: Comment[] }> =>
    api.get(`/blog/posts/${postId}/comments`),
};

// 简历相关API
export const resumeApi = {
  getResume: (): Promise<{ data: ResumeData }> =>
    api.get('/resume'),

  getSections: (sectionType?: string): Promise<{ data: ResumeSection[] }> =>
    api.get('/resume/sections', { params: { section_type: sectionType } }),

  createSection: (section: Partial<ResumeSection>): Promise<{ data: ResumeSection }> =>
    api.post('/resume/sections', section),

  updateSection: (id: number, section: Partial<ResumeSection>): Promise<{ data: ResumeSection }> =>
    api.put(`/resume/sections/${id}`, section),

  deleteSection: (id: number): Promise<void> =>
    api.delete(`/resume/sections/${id}`),
};

// 管理相关API
export const adminApi = {
  getDashboard: (): Promise<{ data: any }> =>
    api.get('/admin/dashboard'),

  getPendingComments: (): Promise<{ data: Comment[] }> =>
    api.get('/admin/comments/pending'),

  approveComment: (id: number): Promise<void> =>
    api.post(`/admin/comments/${id}/approve`),

  deleteComment: (id: number): Promise<void> =>
    api.delete(`/admin/comments/${id}`),

  getMessages: (): Promise<{ data: Message[] }> =>
    api.get('/admin/messages'),

  getMessage: (id: number): Promise<{ data: Message }> =>
    api.get(`/admin/messages/${id}`),

  deleteMessage: (id: number): Promise<void> =>
    api.delete(`/admin/messages/${id}`),

  getUsers: (): Promise<{ data: User[] }> =>
    api.get('/admin/users'),

  toggleUserActive: (id: number): Promise<void> =>
    api.post(`/admin/users/${id}/toggle-active`),
};

export default api;