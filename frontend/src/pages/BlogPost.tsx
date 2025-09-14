import { useState, useEffect } from 'react';
import { useParams, Link, Navigate } from 'react-router-dom';
import { blogApi } from '../services/api';
import type { BlogPost as BlogPostType, Comment } from '../types';

const BlogPost = () => {
  const { slug } = useParams<{ slug: string }>();
  const [post, setPost] = useState<BlogPostType | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [commentForm, setCommentForm] = useState({
    author_name: '',
    author_email: '',
    content: ''
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (slug) {
      fetchPost();
    }
  }, [slug]);

  const fetchPost = async () => {
    setLoading(true);
    try {
      const response = await blogApi.getPost(slug!);
      setPost(response.data);
      
      // 获取评论
      const commentsResponse = await blogApi.getPostComments(response.data.id);
      setComments(commentsResponse.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || '获取文章失败');
    } finally {
      setLoading(false);
    }
  };

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      await blogApi.createComment({
        post_id: post!.id,
        ...commentForm
      });

      // 清空表单
      setCommentForm({
        author_name: '',
        author_email: '',
        content: ''
      });

      // 重新获取评论
      const commentsResponse = await blogApi.getPostComments(post!.id);
      setComments(commentsResponse.data);

      alert('评论提交成功，等待审核后显示');
    } catch (err: any) {
      alert(err.response?.data?.detail || '提交评论失败');
    } finally {
      setSubmitting(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setCommentForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (error === '文章未找到') {
    return <Navigate to="/not-found" replace />;
  }

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

  if (!post) {
    return <Navigate to="/not-found" replace />;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* 返回按钮 */}
      <Link 
        to="/blog" 
        className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-8"
      >
        ← 返回博客列表
      </Link>

      {/* 文章内容 */}
      <article className="mb-12">
        <header className="mb-8">
          {post.category && (
            <span 
              className="inline-block px-4 py-2 text-sm font-semibold text-white rounded-full mb-4"
              style={{ backgroundColor: post.category.color }}
            >
              {post.category.name}
            </span>
          )}
          
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {post.title}
          </h1>

          <div className="flex items-center text-gray-600 text-sm mb-6">
            <span className="mr-4">👁️ {post.view_count} 次阅读</span>
            <span>{new Date(post.created_at).toLocaleDateString()}</span>
          </div>

          {post.featured_image && (
            <img 
              src={post.featured_image} 
              alt={post.title}
              className="w-full h-64 object-cover rounded-lg mb-6"
            />
          )}
        </header>

        <div className="prose prose-lg max-w-none">
          {post.summary && (
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-8">
              <p className="text-blue-800 font-semibold">摘要: {post.summary}</p>
            </div>
          )}

          <div 
            className="text-gray-800 leading-relaxed"
            dangerouslySetInnerHTML={{ __html: post.content.replace(/\n/g, '<br/>') }}
          />
        </div>
      </article>

      {/* 评论部分 */}
      <section className="border-t pt-8">
        <h2 className="text-2xl font-bold mb-6">评论 ({comments.length})</h2>

        {/* 评论列表 */}
        {comments.length > 0 ? (
          <div className="space-y-6 mb-8">
            {comments.map((comment) => (
              <div key={comment.id} className="bg-gray-50 rounded-lg p-6">
                <div className="flex items-center justify-between mb-3">
                  <div className="font-semibold text-gray-900">
                    {comment.author_name}
                  </div>
                  <span className="text-sm text-gray-500">
                    {new Date(comment.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-gray-700">{comment.content}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 mb-8">暂无评论</p>
        )}

        {/* 评论表单 */}
        <div className="bg-white rounded-lg border p-6">
          <h3 className="text-lg font-semibold mb-4">发表评论</h3>
          
          <form onSubmit={handleCommentSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="author_name" className="block text-sm font-medium text-gray-700 mb-2">
                  姓名 *
                </label>
                <input
                  type="text"
                  id="author_name"
                  name="author_name"
                  required
                  value={commentForm.author_name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="请输入您的姓名"
                />
              </div>

              <div>
                <label htmlFor="author_email" className="block text-sm font-medium text-gray-700 mb-2">
                  邮箱 *
                </label>
                <input
                  type="email"
                  id="author_email"
                  name="author_email"
                  required
                  value={commentForm.author_email}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="请输入您的邮箱"
                />
              </div>
            </div>

            <div>
              <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
                评论内容 *
              </label>
              <textarea
                id="content"
                name="content"
                required
                rows={4}
                value={commentForm.content}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入您的评论内容"
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {submitting ? '提交中...' : '提交评论'}
            </button>

            <p className="text-sm text-gray-500">
              注意：所有评论需要管理员审核后才能显示
            </p>
          </form>
        </div>
      </section>
    </div>
  );
};

export default BlogPost;