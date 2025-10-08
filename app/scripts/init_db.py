#!/usr/bin/env python3
"""数据库初始化脚本"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database import create_tables, engine
from app.models import User, PersonalInfo, Experience, ResumeSection, SectionType, Education, BlogCategory, BlogPost, Comment, Message
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
            print(f"管理员用户创建成功: admin/admin123")
            print("警告：请首次登录后立即修改密码！")
        
        # 创建个人信息初始数据
        print("正在创建默认个人信息...")
        
        # 检查是否已有个人信息
        existing_personal_info = db.query(PersonalInfo).count()
        if existing_personal_info == 0:
            personal_info = PersonalInfo(
                name="徐海涛",
                email="xht.pub@gmail.com",
                telephone="176-0218-7958",
                address="上海市闵行区",
                bio="c++后端开发工程师",
                #website="https://example.com",
                github="https://github.com/Learner-XU/",
                #linkedin="https://linkedin.com/in/zhangsan"
            )
            db.add(personal_info)
            db.commit()
            print("个人信息创建成功")
        
        # 创建教育背景初始数据
        print("正在创建默认教育背景数据...")
        
        # 检查是否已有教育背景数据
        existing_education = db.query(Education).count()
        if existing_education == 0:
            education_records = [
                Education(
                    school_name="华东理工大学",
                    degree="硕士",
                    major="机械工程",
                    start_date="2018-09",
                    end_date="2021-06",
                    #gpa="3.8/4.0",
                    description="荣誉/奖项：校级一等奖学金、校级优秀毕业生、“华为杯”第十六届中国研究生数学建模竞赛国家二等奖等",
                    order_index=1
                ),
                Education(
                    school_name="南京工程学院",
                    degree="学士",
                    major="机械设计制造及其自动化",
                    start_date="2012-09",
                    end_date="2016-06",
                    #gpa="3.7/4.0",
                    description="荣誉/奖项：优秀学生（2次）、优秀学生干部（2次）、校级一等奖学金（3次）",
                    order_index=2
                )
            ]
            
            db.add_all(education_records)
            print("教育背景数据创建完成!")
        
        # 创建工作经历初始数据
        print("正在创建默认工作经历数据...")
        
        # 检查是否已有工作经历数据
        existing_experience = db.query(Experience).count()
        if existing_experience == 0:
            experience_records = [
                Experience(
                    company="万得信息技术股份有限公司",
                    position="高级后端开发工程师",
                    start_date="2021-06",
                    #end_date="2025-10",
                    description="负责商品、衍生品实时行情衍生指标计算服务的架构设计与开发、优化系统性能、主导团队技术分享与新人培训",
                    is_visible=True,
                    order_index=1
                )
            ]
            
            db.add_all(experience_records)
            print("工作经历数据创建完成!")
        
        # 创建简历章节初始数据
        print("正在创建默认简历章节数据...")
        
        # 检查是否已有简历章节数据
        existing_sections = db.query(ResumeSection).count()
        if existing_sections == 0:
            resume_sections = [
                ResumeSection(
                    section_type=SectionType.skills,
                    title="技术技能",
                    content="Python, FastAPI, Django\\nMySQL, Redis, MongoDB\\nDocker, Kubernetes, AWS",
                    order_index=4
                ),
                ResumeSection(
                    section_type=SectionType.projects,
                    title="项目经验",
                    content="1. 电商平台后端开发\\n2. 微服务架构设计\\n3. 自动化部署系统",
                    order_index=5
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