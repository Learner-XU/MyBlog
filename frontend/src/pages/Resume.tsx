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
      <div className="resume-container">
        {/* Left Sidebar - Personal Info */}
        <aside className="resume-left-sidebar">
          {/* Profile Section */}
          <div className="resume-profile">
            <div className="resume-avatar">
              <div className="resume-avatar-placeholder">
                <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                  <circle cx="40" cy="40" r="40" fill="#667eea"/>
                  <circle cx="40" cy="30" r="12" fill="white"/>
                  <path d="M20 65c0-11 9-20 20-20s20 9 20 20" fill="white"/>
                </svg>
              </div>
            </div>
            <div className="resume-profile-info">
              <h1 className="resume-name">{resume.personal_info?.name || '姓名'}</h1>
              <p className="resume-title">C++后端开发工程师</p>
              <p className="resume-summary">{resume.personal_info?.bio || '专注于金融科技领域的高性能系统开发'}</p>
            </div>
          </div>

          {/* Contact Info */}
          <section className="resume-sidebar-section">
            <h3 className="resume-sidebar-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
              </svg>
              联系方式
            </h3>
            <div className="resume-contact-list">
              {resume.personal_info && (
                <div className="resume-contact-info">
                  {resume.personal_info.email && (
                    <div className="resume-contact-item">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                      </svg>
                      <span>{resume.personal_info.email}</span>
                    </div>
                  )}
                  {resume.personal_info.telephone && (
                    <div className="resume-contact-item">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                      </svg>
                      <span>{resume.personal_info.telephone}</span>
                    </div>
                  )}
                  {resume.personal_info.address && (
                    <div className="resume-contact-item">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                      </svg>
                      <span>{resume.personal_info.address}</span>
                    </div>
                  )}
                  {resume.personal_info.website && (
                    <div className="resume-contact-item">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                      </svg>
                      <span>{resume.personal_info.website}</span>
                    </div>
                  )}
                  {resume.personal_info.github && (
                    <div className="resume-contact-item">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                      </svg>
                      <span>{resume.personal_info.github}</span>
                    </div>
                  )}
                  {resume.personal_info.linkedin && (
                    <div className="resume-contact-item">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                      </svg>
                      <span>{resume.personal_info.linkedin}</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          </section>



          {/* Skills */}
          <section className="resume-sidebar-section">
            <h3 className="resume-sidebar-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>
              </svg>
              技术技能
            </h3>
            <div className="resume-skills">
              {resume.skills?.map((skill) => (
                <div key={skill.id} className="resume-skill-item">
                  <h4 className="resume-skill-title">{skill.title}</h4>
                  {skill.content && (
                    <div className="resume-skill-bar">
                      <div className="resume-skill-progress" style={{width: '85%'}}></div>
                    </div>
                  )}
                  {skill.content && (
                    <p className="resume-skill-description">{skill.content}</p>
                  )}
                </div>
              ))}
            </div>
          </section>
        </aside>

        {/* Right Main Content */}
        <main className="resume-main-content">
          {/* Education */}
          <section className="resume-section">
            <h2 className="resume-section-title">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82zM12 3L1 9l11 6 9-4.91V17h2V9L12 3z"/>
              </svg>
              教育背景
            </h2>
            <div className="resume-education-main">
              {resume.education
                ?.sort((a, b) => a.order_index - b.order_index)
                .map((edu) => (
                <div key={edu.id} className="resume-education-card">
                  {edu.content && (
                    <div className="resume-education-content">
                      {edu.content.split('\n').map((line, i) => (
                        <p key={i}>{line}</p>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>

          {/* Experience */}
          <section className="resume-section">
            <h2 className="resume-section-title">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20 6h-2.18c.11-.31.18-.65.18-1a2.996 2.996 0 0 0-5.5-1.65l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1z"/>
              </svg>
              工作经历
            </h2>
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
            <h2 className="resume-section-title">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
              项目经验
            </h2>
            <div className="resume-projects-grid">
              {resume.projects?.map((project) => (
                <div key={project.id} className="resume-project-card">
                  <div className="resume-project-header">
                    <h3 className="resume-project-title">{project.title}</h3>
                    <div className="resume-project-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                      </svg>
                    </div>
                  </div>
                  {project.content && (
                    <div className="resume-project-content">
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
      </div>
    </div>
  );
};

export default Resume;