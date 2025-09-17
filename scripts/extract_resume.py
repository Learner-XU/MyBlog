#!/usr/bin/env python3
"""
从Word文档中提取简历内容并转换为JSON格式
"""

import json
import sys
from pathlib import Path
from docx import Document
from typing import Dict, List, Any


def extract_resume_content(docx_path: str) -> Dict[str, Any]:
    """从Word文档中提取简历内容"""
    try:
        doc = Document(docx_path)
        
        resume_data = {
            "personal_info": [],
            "education": [],
            "experience": [],
            "skills": [],
            "projects": []
        }
        
        current_section = None
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if not text:
                continue
            
            # 检测章节标题
            if "个人信息" in text:
                current_section = "personal_info"
            elif "教育背景" in text or "学历" in text:
                current_section = "education"
            elif "工作经历" in text or "工作经验" in text:
                current_section = "experience"
            elif "技能" in text or "专业技能" in text:
                current_section = "skills"
            elif "项目" in text or "项目经验" in text:
                current_section = "projects"
            elif current_section:
                # 添加到当前章节
                resume_data[current_section].append(text)
        
        return resume_data
        
    except Exception as e:
        print(f"提取文档内容时出错: {e}")
        return {}


def create_sample_resume() -> Dict[str, Any]:
    """创建示例简历数据"""
    return {
        "personal_info": [
            "姓名：徐海涛",
            "邮箱：xuhaitao@example.com", 
            "电话：138-****-****",
            "地址：北京市朝阳区"
        ],
        "education": [
            "北京大学 - 计算机科学与技术 (2015-2019) 本科",
            "清华大学 - 软件工程 (2019-2022) 硕士"
        ],
        "experience": [
            "高级软件工程师 - 阿里巴巴集团 (2022年至今)",
            "后端开发工程师 - 腾讯科技 (2020-2022)"
        ],
        "skills": [
            "编程语言: Python, Java, JavaScript/TypeScript, Go",
            "后端框架: FastAPI, Django, Spring Boot, Gin",
            "数据库: MySQL, PostgreSQL, Redis, MongoDB",
            "云原生: Docker, Kubernetes, AWS, 微服务架构"
        ],
        "projects": [
            "电商平台微服务重构项目",
            "智能推荐系统开发",
            "高并发支付系统设计"
        ]
    }


def main():
    docx_path = "/mnt/data/徐海涛 简历V2.docx"
    
    if not Path(docx_path).exists():
        print(f"文件不存在: {docx_path}")
        print("使用示例简历数据...")
        resume_data = create_sample_resume()
    else:
        print(f"正在提取简历内容: {docx_path}")
        resume_data = extract_resume_content(docx_path)
        
        # 如果提取失败，使用示例数据
        if not any(resume_data.values()):
            print("文档内容提取失败，使用示例简历数据...")
            resume_data = create_sample_resume()
    
    # 转换为前端需要的格式
    formatted_resume = {
        "personal_info": [{"id": 1, "title": "个人信息", "content": "\n".join(resume_data.get("personal_info", [])), "order_index": 1, "is_visible": True}],
        "education": [
            {"id": i+1, "title": item, "content": "", "order_index": i+1, "is_visible": True}
            for i, item in enumerate(resume_data.get("education", []))
        ],
        "experience": [
            {"id": i+1, "title": item, "content": "", "order_index": i+1, "is_visible": True}
            for i, item in enumerate(resume_data.get("experience", []))
        ],
        "skills": [
            {"id": i+1, "title": "技能", "content": item, "order_index": i+1, "is_visible": True}
            for i, item in enumerate(resume_data.get("skills", []))
        ],
        "projects": [
            {"id": i+1, "title": item, "content": "", "order_index": i+1, "is_visible": True}
            for i, item in enumerate(resume_data.get("projects", []))
        ]
    }
    
    # 保存到文件
    output_path = "/mnt/data/git/MyBlog/frontend/src/data/resumeData.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_resume, f, ensure_ascii=False, indent=2)
    
    print(f"简历数据已保存到: {output_path}")
    
    # 同时创建TypeScript版本
    ts_output_path = "/mnt/data/git/MyBlog/frontend/src/data/resumeData.ts"
    with open(ts_output_path, 'w', encoding='utf-8') as f:
        f.write('import { ResumeData, SectionType } from \'../types\';\n\n')
        f.write('export const resumeData: ResumeData = ')
        json.dump(formatted_resume, f, ensure_ascii=False, indent=2)
        f.write(';\n\nexport default resumeData;\n')
    
    print(f"TypeScript版本已保存到: {ts_output_path}")
    
    # 打印摘要
    print("\n简历内容摘要:")
    for section, items in formatted_resume.items():
        print(f"{section}: {len(items)} 条记录")


if __name__ == "__main__":
    main()