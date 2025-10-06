import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Header = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? 'nav-link active' : 'nav-link';
  };

  const headerStyle: React.CSSProperties = {
    backgroundColor: '#ffffff',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    borderBottom: '1px solid #e5e7eb',
    position: 'sticky',
    top: 0,
    zIndex: 1000
  };

  const containerStyle: React.CSSProperties = {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 1.5rem',
    height: '4rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between'
  };

  const logoStyle: React.CSSProperties = {
    fontSize: '1.75rem',
    fontWeight: 'bold',
    background: 'linear-gradient(135deg, #2563eb, #7c3aed)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    textDecoration: 'none',
    transition: 'all 0.2s ease'
  };

  const navStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '2rem'
  };

  const userAreaStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem'
  };

  const buttonStyle: React.CSSProperties = {
    padding: '0.5rem 1rem',
    borderRadius: '0.5rem',
    border: 'none',
    fontWeight: '500',
    textDecoration: 'none',
    transition: 'all 0.2s ease',
    cursor: 'pointer',
    fontSize: '0.875rem',
    boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
  };

  const loginButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#2563eb',
    color: 'white'
  };

  const logoutButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#dc2626',
    color: 'white'
  };

  const welcomeTextStyle: React.CSSProperties = {
    fontSize: '0.875rem',
    color: '#6b7280',
    fontWeight: '500'
  };

  const usernameStyle: React.CSSProperties = {
    color: '#2563eb',
    fontWeight: '600'
  };

  return (
    <header style={headerStyle}>
      <div style={containerStyle}>
        {/* Logo区域 */}
        <div>
          <Link to="/" style={logoStyle}>
            MyBlog
          </Link>
        </div>
        
        {/* 导航菜单区域 */}
        <nav style={navStyle}>
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

        {/* 用户操作区域 */}
        <div style={userAreaStyle}>
          {user ? (
            <>
              <span style={welcomeTextStyle}>
                欢迎, <span style={usernameStyle}>{user.username}</span>
              </span>
              <button
                onClick={logout}
                style={logoutButtonStyle}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#b91c1c';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                  e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = '#dc2626';
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
                }}
              >
                退出
              </button>
            </>
          ) : (
            <Link
              to="/login"
              style={loginButtonStyle}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#1d4ed8';
                e.currentTarget.style.transform = 'translateY(-1px)';
                e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = '#2563eb';
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
              }}
            >
              登录
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;