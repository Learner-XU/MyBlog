import { ResumeData, SectionType } from '../types';

const now = new Date().toISOString();

export const resumeData: ResumeData = {
  personal_info: {
    id: 1,
    name: '徐海涛',
    email: 'xuhaitao@example.com',
    telephone: '138-****-****',
    address: '上海市浦东新区',
    bio: '专注于金融科技领域的高性能系统开发，具有丰富的C++后端开发经验',
    website: 'https://xuhaitao.dev',
    github: 'https://github.com/xuhaitao',
    linkedin: 'https://linkedin.com/in/xuhaitao',
    is_visible: true,
    created_at: now,
    updated_at: now
  },
  education: [
    {
      id: 2,
      school_name: '清华大学',
      degree: '硕士',
      major: '软件工程',
      start_date: '2019-09',
      end_date: '2022-06',
      gpa: '3.8/4.0',
      description: '研究方向：人工智能与机器学习\n主要研究：深度学习算法优化、自然语言处理\n获得优秀毕业生称号',
      order_index: 1,
      is_visible: true,
      created_at: now,
      updated_at: now
    },
    {
      id: 13,
      school_name: '北京大学',
      degree: '学士',
      major: '计算机科学与技术',
      start_date: '2015-09',
      end_date: '2019-06',
      gpa: '3.7/4.0',
      description: '主修课程：算法设计、数据结构、操作系统、计算机网络\n参与ACM竞赛，获得区域赛银奖',
      order_index: 2,
      is_visible: true,
      created_at: now,
      updated_at: now
    }
  ],
  experience: [
    {
      id: 3,
      section_type: SectionType.experience,
      title: 'C++后端开发工程师 - 万得信息技术股份有限公司',
      content: '2021.06 – 至今\n• 负责金融数据平台后端系统开发\n• 设计和实现高并发数据处理系统\n• 优化系统性能，提升数据处理效率',
      order_index: 1,
      is_visible: true,
      created_at: now,
      updated_at: now
    },
    {
      id: 4,
      section_type: SectionType.experience,
      title: '爬虫开发工程师 - 金融数据采集',
      content: '2020-2021\n• 参与爬虫脚本开发和维护\n• 结构化业务数据处理\n• SQL数据库设计和优化',
      order_index: 2,
      is_visible: true,
      created_at: now,
      updated_at: now
    }
  ],
  skills: [
    {
      id: 5,
      section_type: SectionType.skills,
      title: '编程语言',
      content: '扎实的C/C++编程功底，熟悉C++11新特性，熟悉STL，Python',
      order_index: 1,
      is_visible: true,
      created_at: now,
      updated_at: now
    },
    {
      id: 6,
      section_type: SectionType.skills,
      title: '操作系统',
      content: '熟练掌握UNIX/Linux环境，熟悉进程/线程管理、IPC、内存管理',
      order_index: 2,
      is_visible: true,
      created_at: now,
      updated_at: now
    },
    {
      id: 7,
      section_type: SectionType.skills,
      title: '网络编程',
      content: 'Linux多线程编程、并发网络编程，熟悉I/O复用（select/poll/epoll）模型',
      order_index: 3,
      is_visible: true,
      created_at: now,
      updated_at: now
    },
    {
      id: 8,
      section_type: SectionType.skills,
      title: '数据库',
      content: '熟悉MySQL、Oracle数据库，SQL编写与优化',
      order_index: 4,
      is_visible: true,
      created_at: now,
      updated_at: now
    },
    {
      id: 9,
      section_type: SectionType.skills,
      title: '数据结构与算法',
      content: '熟悉常用数据结构和算法，了解设计模式',
      order_index: 5,
      is_visible: true,
      created_at: now,
      updated_at: now
    }
  ],
  projects: [
    {
      id: 10,
      section_type: SectionType.projects,
      title: '金融期权指标计算系统',
      content: '• 开发期权希腊字母指标计算模块（IV、Delta、Gamma、Vega等）\n• 基于TBB多线程库并行计算，提升计算性能\n• 集成EXPO、TD、Cloud等API封装',
      order_index: 1,
      is_visible: true,
      created_at: now,
      updated_at: now
    },
    {
      id: 11,
      section_type: SectionType.projects,
      title: '高并发网络通信系统',
      content: '• 基于Reactor模式开发网络通信模块（Libevent）\n• 实现数据序列化（Protobuf）和高效传输\n• 支持多线程场景配置和优化',
      order_index: 2,
      is_visible: true,
      created_at: now,
      updated_at: now
    },
    {
      id: 12,
      section_type: SectionType.projects,
      title: '自动化部署系统',
      content: '• 开发Shell脚本实现自动化部署\n• 集成SVN代码管理和版本控制\n• 实现持续集成和自动化测试',
      order_index: 3,
      is_visible: true,
      created_at: now,
      updated_at: now
    }
  ]
};

export default resumeData;