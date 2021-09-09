
from pytrader.database import async_db_session
import sqlalchemy as sa


class ModelAdmin:
  @classmethod
  async def create(cls, **kwargs):
    async_db_session.add(cls(**kwargs))
    await async_db_session.commit()

  @classmethod
  async def update(cls, id, **kwargs):
    query = (
      sa.update(cls)
      .where(cls.id == id)
      .values(**kwargs)
      .execution_options(synchronize_session="fetch")
    )

    await async_db_session.execute(query)
    await async_db_session.commit()

  @classmethod
  async def get(cls, id):
    query = sa.future.select(cls).where(cls.id == id)
    results = await async_db_session.execute(query)
    (result,) = results.one()
    return result
