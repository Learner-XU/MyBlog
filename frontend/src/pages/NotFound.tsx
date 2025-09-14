import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-gray-700 mb-8">页面未找到</h2>
        <p className="text-gray-600 mb-8 max-w-md">
          抱歉，您访问的页面不存在。可能是URL地址输入错误，或者页面已被移除。
        </p>
        <div className="space-x-4">
          <Link
            to="/"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            返回首页
          </Link>
          <Link
            to="/blog"
            className="border-2 border-blue-600 text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-600 hover:text-white transition-colors"
          >
            浏览博客
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;