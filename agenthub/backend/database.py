"""
数据库配置和会话管理
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

# 从环境变量读取数据库 URL，默认使用 SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./agenthub.db"
)

# 如果是 PostgreSQL，启用连接池
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600
    )
else:
    # SQLite
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """初始化数据库，创建所有表"""
    from models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def get_db() -> Session:
    """
    FastAPI 依赖注入：获取数据库会话
    使用 yield 确保会话在请求结束后关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    上下文管理器：用于非 FastAPI 环境的数据库访问
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def reset_db():
    """重置数据库（仅用于开发/测试）"""
    from models import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("⚠️ Database reset complete")
