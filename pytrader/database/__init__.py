
import pytrader.config as cfg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

DB = {
  'host': cfg.get('DB_HOST'),
  'user': cfg.get('DB_USER'),
  'password': cfg.get('DB_PASS'),
  'database': cfg.get('DB_NAME'),
}

DSN=f"postgresql+asyncpg://{DB['user']}:{DB['password']}@{DB['host']}/{DB['database']}-dev"


class AsyncDatabaseSession:
  def __init__(self):
    self._session = None
    self._engine = None

  def __getattr__(self, name):
    return getattr(self._session, name)

  async def init(self):
    self._engine = create_async_engine(DSN, echo=True)

    self._session = sessionmaker(
      self._engine, expire_on_commit=False, class_=AsyncSession
    )()

  async def create_all(self):
    async with self._engine.begin() as conn:
      await conn.run_sync(Base.metadata.drop_all)
      await conn.run_sync(Base.metadata.create_all)


async_db_session = AsyncDatabaseSession()
