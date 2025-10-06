#!/usr/bin/env python3
"""数据库初始化脚本"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database import create_tables, engine
from app.models import User, PersonalInfo, ResumeSection, SectionType, BlogCategory, BlogPost, Comment, Message
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash


def init_database():
    """初始化数据库，创建所有表"""
    print("正在创建数据库表...")
    create_tables()
    print("数据库表创建完成!")


def create_initial_data():
    """创建初始数据"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 检查是否已有管理员用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("正在创建默认管理员用户...")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                full_name="Administrator",
                password_hash=get_password_hash("admin123")
            )
            db.add(admin_user)
            db.commit()
            print(f"管理员用户创建成功: admin/admin123")
        
        # 创建个人信息初始数据
        print("正在创建默认个人信息...")
        
        # 检查是否已有个人信息
        existing_personal_info = db.query(PersonalInfo).count()
        if existing_personal_info == 0:
            personal_info = PersonalInfo(
                name="张三",
                email="zhangsan@example.com",
                telephone="138-****-****",
                address="北京市朝阳区",
                bio="全栈开发工程师，专注于Web应用开发",
                website="https://example.com",
                github="https://github.com/zhangsan",
                linkedin="https://linkedin.com/in/zhangsan"
            )
            db.add(personal_info)
            db.commit()
            print("个人信息创建成功")
        
        # 创建简历章节初始数据
        print("正在创建默认简历章节数据...")
        
        # 检查是否已有简历章节数据
        existing_sections = db.query(ResumeSection).count()
        if existing_sections == 0:
            resume_sections = [
                ResumeSection(
                    section_type=SectionType.education,
                    title="硕士学历",
                    content="计算机科学与技术 硕士学位\n2019年9月 - 2022年6月\n清华大学",
                    order_index=1
                ),
                ResumeSection(
                    section_type=SectionType.education,
                    title="本科学历",
                    content="软件工程 学士学位\n2015年9月 - 2019年6月\n北京大学",
                    order_index=2
                ),
                ResumeSection(
                    section_type=SectionType.experience,
                    title="工作经历",
                    content="2022-至今 某某科技公司 高级软件工程师\\n2020-2022 某某互联网公司 后端开发工程师",
                    order_index=4
                ),
                ResumeSection(
                    section_type=SectionType.skills,
                    title="技术技能",
                    content="Python, FastAPI, Django\\nMySQL, Redis, MongoDB\\nDocker, Kubernetes, AWS",
                    order_index=5
                ),
                ResumeSection(
                    section_type=SectionType.projects,
                    title="项目经验",
                    content="1. 电商平台后端开发\\n2. 微服务架构设计\\n3. 自动化部署系统",
                    order_index=6
                )
            ]
            
            db.add_all(resume_sections)
            print("简历数据创建完成!")
        
        # 创建博客分类
        existing_categories = db.query(BlogCategory).count()
        if existing_categories == 0:
            categories = [
                BlogCategory(name="技术文章", slug="technology", description="技术相关的文章"),
                BlogCategory(name="生活随笔", slug="life", description="生活感悟和随笔"),
                BlogCategory(name="读书笔记", slug="reading", description="读书笔记和心得")
            ]
            db.add_all(categories)
            print("博客分类创建完成!")
        
        db.commit()
        
    except Exception as e:
        print(f"创建初始数据时发生错误: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """主函数"""
    print("=== MyBlog 数据库初始化 ===")
    
    try:
        init_database()
        create_initial_data()
        print("\n=== 数据库初始化完成 ===")
        print("管理员账号: admin/admin123")
        print("请及时修改默认密码!")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()