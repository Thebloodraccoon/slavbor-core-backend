import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from redis.asyncio import Redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models import Race
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


@pytest.fixture
def create_race(db_session):
    """Factory fixture for creating races in database"""

    def _create_race(
        name="Test name",
        description="Test description",
        size="Средний",
        special_traits="Test special traits",
        is_playable=True,
        rarity="обычная",
    ):
        existing_race = db_session.query(Race).filter_by(name=name).first()
        if existing_race:
            return existing_race

        race = Race(
            name=name,
            description=description,
            size=size,
            special_traits=special_traits,
            is_playable=is_playable,
            rarity=rarity,
        )

        db_session.add(race)
        db_session.commit()
        db_session.refresh(race)

        return race

    return _create_race


@pytest.fixture
def test_race(create_race):
    """Default test race"""
    return create_race()
