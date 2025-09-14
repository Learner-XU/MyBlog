import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
from app.core.security import get_password_hash
from app.models.user import User

# 测试客户端
client = TestClient(app)

# 测试数据库设置
@pytest.fixture(scope="module")
def test_db():
    # 创建测试表
    Base.metadata.create_all(bind=engine)
    
    # 创建测试数据
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # 创建测试用户
    test_user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        password_hash=get_password_hash("testpassword")
    )
    db.add(test_user)
    db.commit()
    
    yield db
    
    # 清理
    db.delete(test_user)
    db.commit()
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_login_success(test_db):
    """测试成功登录"""
    response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure(test_db):
    """测试登录失败"""
    response = client.post("/api/auth/login", data={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401


def test_protected_endpoint_without_token(test_db):
    """测试未认证访问受保护端点"""
    response = client.get("/api/auth/me")
    
    assert response.status_code == 401


def test_protected_endpoint_with_token(test_db):
    """测试认证访问受保护端点"""
    # 先获取token
    login_response = client.post("/api/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    
    token = login_response.json()["access_token"]
    
    # 使用token访问受保护端点
    response = client.get("/api/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"