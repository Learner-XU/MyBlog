#!/usr/bin/env python3
"""
简易API服务器 - 使用Python内置模块
提供基本的API接口供前端调用
"""

import json
import sqlite3
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SimpleAPIHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 设置CORS头
        self.send_cors_headers()
        
        if path == '/api/health':
            self.send_json_response({"status": "healthy", "service": "simple_api"})
        
        elif path == '/api/blog/posts':
            # 模拟博客文章数据
            posts = [
                {
                    "id": 1,
                    "title": "欢迎来到MyBlog",
                    "slug": "welcome-to-myblog",
                    "summary": "这是我的第一篇博客文章，欢迎来到我的个人博客网站！",
                    "view_count": 42,
                    "is_published": True,
                    "created_at": "2024-01-01T10:00:00",
                    "category": {"name": "技术文章", "color": "#007bff"}
                },
                {
                    "id": 2, 
                    "title": "React开发最佳实践",
                    "slug": "react-best-practices",
                    "summary": "分享一些React开发中的最佳实践和经验",
                    "view_count": 28,
                    "is_published": True,
                    "created_at": "2024-01-02T14:30:00",
                    "category": {"name": "技术文章", "color": "#007bff"}
                }
            ]
            self.send_json_response({
                "items": posts,
                "total": len(posts),
                "page": 1,
                "size": 10,
                "pages": 1
            })
        
        elif path == '/api/resume':
            # 模拟简历数据
            resume_data = {
                "personal_info": [
                    {
                        "title": "个人信息",
                        "content": "姓名：张三\\n邮箱：zhangsan@example.com\\n电话：138-****-****\\n地址：北京市朝阳区"
                    }
                ],
                "education": [
                    {
                        "title": "教育背景", 
                        "content": "2015-2019 北京大学 计算机科学与技术 本科\\n2019-2022 清华大学 软件工程 硕士"
                    }
                ],
                "experience": [
                    {
                        "title": "工作经历",
                        "content": "2022-至今 某某科技公司 高级软件工程师\\n2020-2022 某某互联网公司 后端开发工程师"
                    }
                ],
                "skills": [
                    {
                        "title": "技术技能",
                        "content": "Python, FastAPI, Django\\nMySQL, Redis, MongoDB\\nDocker, Kubernetes, AWS"
                    }
                ],
                "projects": [
                    {
                        "title": "项目经验", 
                        "content": "1. 电商平台后端开发\\n2. 微服务架构设计\\n3. 自动化部署系统"
                    }
                ]
            }
            self.send_json_response(resume_data)
        
        elif path == '/':
            self.send_json_response({
                "message": "MyBlog简易API服务器",
                "version": "1.0.0",
                "endpoints": [
                    "/api/health",
                    "/api/blog/posts", 
                    "/api/resume"
                ]
            })
        
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_cors_headers()
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        """处理POST请求"""
        self.send_cors_headers()
        
        if self.path == '/api/auth/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # 模拟登录验证
            if data.get('username') == 'admin' and data.get('password') == 'admin123':
                self.send_json_response({
                    "access_token": "mock-jwt-token-12345",
                    "token_type": "bearer",
                    "user": {
                        "id": 1,
                        "username": "admin",
                        "full_name": "Administrator"
                    }
                })
            else:
                self.send_error(401, "用户名或密码错误")
        else:
            self.send_error(404, "Endpoint not found")
    
    def send_cors_headers(self):
        """发送CORS头"""
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3001')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Credentials', 'true')
    
    def send_json_response(self, data, status=200):
        """发送JSON响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))

def run_server():
    """启动服务器"""
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    
    print("🚀 简易API服务器启动成功！")
    print("📍 服务地址: http://localhost:8000")
    print("🔗 前端地址: http://localhost:3001")
    print("📋 可用接口:")
    print("   GET  /api/health        健康检查")
    print("   GET  /api/blog/posts    博客文章")
    print("   GET  /api/resume        简历数据")
    print("   POST /api/auth/login    用户登录")
    print("\n⏹️  按 Ctrl+C 停止服务器")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")

if __name__ == '__main__':
    run_server()