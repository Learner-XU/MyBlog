import { useState, useEffect } from 'react';
import { resumeApi } from '../services/api';
import type { ResumeData } from '../types';
import './Resume.css';

const Resume = () => {
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchResume();
  }, []);

  const fetchResume = async () => {
    setLoading(true);
    try {
      const response = await resumeApi.getResume();
      setResume(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || '获取简历失败');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="resume-loading">
        <div className="resume-spinner"></div>
        <p>正在加载简历...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="resume-container">
        <div className="resume-error">
          <h2>⚠️</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!resume) {
    return (
      <div className="resume-container">
        <div className="resume-empty">
          <h2>📄</h2>
          <p>暂无简历内容</p>
        </div>
      </div>
    );
  }

  return (
    <div className="resume">
      {/* Header */}
      <header className="resume-header">
        <div className="resume-header-content">
          <h1 className="resume-name">徐海涛</h1>
          <p className="resume-title">C++后端开发工程师</p>
          <p className="resume-summary">专注于金融科技领域的高性能系统开发</p>
        </div>
      </header>

      <div className="resume-content">
        {/* Main Content */}
        <main className="resume-main">
          {/* Experience */}
          <section className="resume-section">
            <h2 className="resume-section-title">💼 工作经历</h2>
            <div className="resume-timeline">
              {resume.experience?.map((exp) => (
                <div key={exp.id} className="resume-timeline-item">
                  <div className="resume-timeline-marker"></div>
                  <div className="resume-timeline-content">
                    <h3 className="resume-timeline-title">{exp.title}</h3>
                    {exp.content && (
                      <div className="resume-timeline-description">
                        {exp.content.split('\n').map((line, i) => (
                          <p key={i}>{line}</p>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Projects */}
          <section className="resume-section">
            <h2 className="resume-section-title">🚀 项目经验</h2>
            <div className="resume-grid">
              {resume.projects?.map((project) => (
                <div key={project.id} className="resume-card">
                  <h3 className="resume-card-title">{project.title}</h3>
                  {project.content && (
                    <div className="resume-card-content">
                      {project.content.split('\n').map((line, i) => (
                        <p key={i}>{line}</p>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        </main>

        {/* Sidebar */}
        <aside className="resume-sidebar">
          {/* Contact Info */}
          <section className="resume-sidebar-section">
            <h3 className="resume-sidebar-title">📧 联系方式</h3>
            {resume.personal_info?.map((info) => (
              <div key={info.id} className="resume-contact-info">
                {info.content && info.content.split('\n').map((line, i) => (
                  <p key={i} className="resume-contact-line">{line}</p>
                ))}
              </div>
            ))}
          </section>

          {/* Skills */}
          <section className="resume-sidebar-section">
            <h3 className="resume-sidebar-title">🛠️ 技术技能</h3>
            <div className="resume-skills">
              {resume.skills?.map((skill) => (
                <div key={skill.id} className="resume-skill-item">
                  <h4 className="resume-skill-title">{skill.title}</h4>
                  {skill.content && (
                    <p className="resume-skill-description">{skill.content}</p>
                  )}
                </div>
              ))}
            </div>
          </section>

          {/* Education */}
          <section className="resume-sidebar-section">
            <h3 className="resume-sidebar-title">🎓 教育背景</h3>
            <div className="resume-education">
              {resume.education?.map((edu) => (
                <div key={edu.id} className="resume-education-item">
                  <h4 className="resume-education-title">{edu.title}</h4>
                  {edu.content && (
                    <p className="resume-education-description">{edu.content}</p>
                  )}
                </div>
              ))}
            </div>
          </section>
        </aside>
      </div>

      {/* Footer */}
      <footer className="resume-footer">
        <p>© 2024 徐海涛 · 专业简历</p>
      </footer>
    </div>
  );
};

export default Resume;