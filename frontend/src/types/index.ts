// API响应类型
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

// 分页响应
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// 用户相关类型
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// 博客相关类型
export interface BlogCategory {
  id: number;
  name: string;
  slug: string;
  description?: string;
  color: string;
  created_at: string;
}

export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  summary?: string;
  content: string;
  category?: BlogCategory;
  author_id: number;
  featured_image?: string;
  is_published: boolean;
  view_count: number;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface BlogPostList {
  id: number;
  title: string;
  slug: string;
  summary?: string;
  category?: BlogCategory;
  view_count: number;
  is_published: boolean;
  created_at: string;
  published_at?: string;
}

export interface Comment {
  id: number;
  post_id: number;
  author_name: string;
  author_email: string;
  content: string;
  is_approved: boolean;
  created_at: string;
}

// 简历相关类型
export enum SectionType {
  personal_info = "personal_info",
  education = "education",
  experience = "experience",
  skills = "skills",
  projects = "projects"
}

export interface PersonalInfo {
  id: number;
  name: string;
  email?: string;
  telephone?: string;
  address?: string;
  avatar_url?: string;
  bio?: string;
  website?: string;
  github?: string;
  linkedin?: string;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface ResumeSection {
  id: number;
  section_type: SectionType;
  title: string;
  content?: string;
  order_index: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface Education {
  id: number;
  school_name: string;
  degree: string;
  major: string;
  start_date: string;
  end_date?: string;
  gpa?: string;
  description?: string;
  order_index: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface ResumeData {
  personal_info?: PersonalInfo;
  education: Education[];
  experience: ResumeSection[];
  skills: ResumeSection[];
  projects: ResumeSection[];
}

// 留言相关类型
export interface Message {
  id: number;
  name: string;
  email: string;
  subject?: string;
  content: string;
  is_read: boolean;
  created_at: string;
}