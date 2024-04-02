from epl_bot.db_utils.db import Base, engine
from sqlalchemy import Column, Integer
from sqlalchemy import DateTime, JSON
from sqlalchemy.sql import func


class PointTable(Base):
    __tablename__ = 'point_table'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    create_date = Column(DateTime(timezone=True), server_default=func.now())


class NewsFeedTable(Base):
    __tablename__ = 'news_feed_table'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    create_date = Column(DateTime(timezone=True), server_default=func.now())


if __name__ == '__main__':
    Base.metadata.create_all(engine)
