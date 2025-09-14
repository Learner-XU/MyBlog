import { useState, useEffect } from 'react';
import { resumeApi } from '../services/api';
import type { ResumeData, SectionType } from '../types';

const Resume = () => {
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [activeTab, setActiveTab] = useState<SectionType>(SectionType.personal_info);
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

  const sectionTitles = {
    [SectionType.personal_info]: '个人信息',
    [SectionType.education]: '教育背景',
    [SectionType.experience]: '工作经历',
    [SectionType.skills]: '技术技能',
    [SectionType.projects]: '项目经验'
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-600 p-4 rounded">
          {error}
        </div>
      </div>
    );
  }

  if (!resume) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-gray-500">暂无简历内容</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* 头部 */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">个人简历</h1>
        <p className="text-xl text-gray-600">专业技能与工作经历</p>
      </div>

      {/* 标签页导航 */}
      <div className="border-b border-gray-200 mb-8">
        <nav className="flex space-x-8">
          {Object.values(SectionType).map((sectionType) => (
            <button
              key={sectionType}
              onClick={() => setActiveTab(sectionType)}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === sectionType
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {sectionTitles[sectionType]}
            </button>
          ))}
        </nav>
      </div>

      {/* 内容区域 */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          {sectionTitles[activeTab]}
        </h2>

        <div className="space-y-6">
          {resume[activeTab]?.map((section) => (
            <div key={section.id} className="border-l-4 border-blue-500 pl-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {section.title}
              </h3>
              {section.content && (
                <div className="text-gray-700 leading-relaxed whitespace-pre-line">
                  {section.content}
                </div>
              )}
            </div>
          ))}

          {(!resume[activeTab] || resume[activeTab].length === 0) && (
            <div className="text-center text-gray-500 py-8">
              暂无{sectionTitles[activeTab]}内容
            </div>
          )}
        </div>
      </div>

      {/* 联系信息 */}
      <div className="mt-12 bg-blue-50 rounded-lg p-6">
        <h3 className="text-xl font-semibold text-blue-900 mb-4">联系我</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-blue-800">
          {resume.personal_info?.map((info) => (
            <div key={info.id} className="flex items-center">
              <span className="text-blue-600 mr-2">•</span>
              {info.content}
            </div>
          ))}
        </div>
      </div>

      {/* 技能概览 */}
      {resume.skills && resume.skills.length > 0 && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">技能概览</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {resume.skills.map((skill) => (
              <div key={skill.id} className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-2">{skill.title}</h4>
                {skill.content && (
                  <p className="text-gray-600 text-sm">{skill.content}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Resume;