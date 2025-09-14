const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">MyBlog</h3>
            <p className="text-gray-300">
              个人简历与博客网站，展示技术文章和个人经历。
            </p>
          </div>

          <div>
            <h4 className="text-lg font-semibold mb-4">快速链接</h4>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-gray-300 hover:text-white">
                  首页
                </a>
              </li>
              <li>
                <a href="/blog" className="text-gray-300 hover:text-white">
                  博客
                </a>
              </li>
              <li>
                <a href="/resume" className="text-gray-300 hover:text-white">
                  简历
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-lg font-semibold mb-4">联系我</h4>
            <div className="space-y-2 text-gray-300">
              <p>📧 example@email.com</p>
              <p>📱 +86 138-****-****</p>
              <p>📍 北京市朝阳区</p>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-6 text-center">
          <p className="text-gray-300">
            © 2024 MyBlog. 保留所有权利。
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;