import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Header = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? 'text-blue-600 font-semibold' : 'text-gray-700 hover:text-blue-600';
  };

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">
            MyBlog
          </Link>

          <nav className="hidden md:flex space-x-8">
            <Link to="/" className={isActive('/')}>
              首页
            </Link>
            <Link to="/blog" className={isActive('/blog')}>
              博客
            </Link>
            <Link to="/resume" className={isActive('/resume')}>
              简历
            </Link>
            {user && (
              <Link to="/admin" className={isActive('/admin')}>
                管理
              </Link>
            )}
          </nav>

          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <span className="text-sm text-gray-600">欢迎, {user.username}</span>
                <button
                  onClick={logout}
                  className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
                >
                  退出
                </button>
              </>
            ) : (
              <Link
                to="/login"
                className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                登录
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;