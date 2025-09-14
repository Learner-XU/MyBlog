import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { blogApi, resumeApi } from '../services/api';
import type { BlogPostList, ResumeData } from '../types';

const Home = () => {
  const [featuredPosts, setFeaturedPosts] = useState<BlogPostList[]>([]);
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 获取最新的3篇博客文章
        const postsResponse = await blogApi.getPosts({
          page: 1,
          size: 3,
          published_only: true
        });
        setFeaturedPosts(postsResponse.data.items);

        // 获取简历信息
        const resumeResponse = await resumeApi.getResume();
        setResume(resumeResponse.data);
      } catch (error) {
        console.error('获取数据失败:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 to-blue-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            欢迎来到我的博客
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100">
            分享技术知识，记录生活点滴
          </p>
          <div className="space-x-4">
            <Link
              to="/blog"
              className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              浏览博客
            </Link>
            <Link
              to="/resume"
              className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
            >
              查看简历
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Posts */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">精选文章</h2>
          
          {featuredPosts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {featuredPosts.map((post) => (
                <article key={post.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="p-6">
                    {post.category && (
                      <span 
                        className="inline-block px-3 py-1 text-xs font-semibold text-white rounded-full mb-4"
                        style={{ backgroundColor: post.category.color }}
                      >
                        {post.category.name}
                      </span>
                    )}
                    <h3 className="text-xl font-semibold mb-3">
                      <Link 
                        to={`/blog/${post.slug}`}
                        className="hover:text-blue-600 transition-colors"
                      >
                        {post.title}
                      </Link>
                    </h3>
                    {post.summary && (
                      <p className="text-gray-600 mb-4 line-clamp-2">
                        {post.summary}
                      </p>
                    )}
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      <span>👁️ {post.view_count} 次阅读</span>
                      <span>{new Date(post.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <p className="text-center text-gray-500">暂无文章</p>
          )}

          <div className="text-center mt-8">
            <Link
              to="/blog"
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              查看所有文章
            </Link>
          </div>
        </div>
      </section>

      {/* About Me Section */}
      {resume?.personal_info && (
        <section className="py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">关于我</h2>
            
            <div className="max-w-2xl mx-auto text-center">
              {resume.personal_info.map((section) => (
                <div key={section.id} className="prose prose-lg mx-auto">
                  <p className="text-gray-700 leading-relaxed">
                    {section.content}
                  </p>
                </div>
              ))}
              
              <div className="mt-8">
                <Link
                  to="/resume"
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                >
                  查看完整简历
                </Link>
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default Home;