import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from redis.asyncio import Redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.settings import settings

test_engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def install_test_extensions():
    """Install required PostgreSQL extensions for testing"""
    try:
        with test_engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gin"))
            conn.commit()
            print("PostgreSQL extensions installed successfully")
    except Exception as e:
        print(f"Warning: Could not install PostgreSQL extensions: {e}")


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    install_test_extensions()

    settings.Base.metadata.create_all(bind=test_engine)
    yield
    settings.Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        for table in reversed(settings.Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db_session, redis_test):
    with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def redis_test():
    redis_client = Redis(
        host=settings.TEST_REDIS_HOST,
        port=settings.TEST_REDIS_PORT,
        db=settings.TEST_REDIS_DB,
        decode_responses=True,
    )
    await redis_client.flushdb()
    yield redis_client
    await redis_client.flushdb()
    await redis_client.aclose()
