import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Admin = () => {
  const { user } = useAuth();

  // 如果没有登录，重定向到登录页
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">管理后台</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* 统计卡片 */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">文章总数</h3>
          <p className="text-3xl font-bold text-blue-600">24</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">待审核评论</h3>
          <p className="text-3xl font-bold text-orange-600">5</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">用户数量</h3>
          <p className="text-3xl font-bold text-green-600">1</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">访问量</h3>
          <p className="text-3xl font-bold text-purple-600">1,234</p>
        </div>
      </div>

      {/* 快速操作 */}
      <div className="mt-8 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">快速操作</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
            新建文章
          </button>
          <button className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors">
            管理分类
          </button>
          <button className="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors">
            审核评论
          </button>
          <button className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 transition-colors">
            查看统计
          </button>
        </div>
      </div>

      {/* 最近活动 */}
      <div className="mt-8 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">最近活动</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2 border-b">
            <div>
              <p className="text-sm text-gray-600">新文章发布</p>
              <p className="text-xs text-gray-500">《深入理解React Hooks》</p>
            </div>
            <span className="text-xs text-gray-500">2小时前</span>
          </div>
          <div className="flex items-center justify-between py-2 border-b">
            <div>
              <p className="text-sm text-gray-600">新评论待审核</p>
              <p className="text-xs text-gray-500">用户: 张三</p>
            </div>
            <span className="text-xs text-gray-500">1小时前</span>
          </div>
          <div className="flex items-center justify-between py-2">
            <div>
              <p className="text-sm text-gray-600">系统更新</p>
              <p className="text-xs text-gray-500">版本升级至v1.2.0</p>
            </div>
            <span className="text-xs text-gray-500">昨天</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Admin;