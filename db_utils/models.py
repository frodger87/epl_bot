from epl_bot.db_utils.db import Base, engine
from sqlalchemy import Column, Integer, DateTime, JSON, String, Boolean
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


class FixturesTable(Base):
    __tablename__ = 'fixtures'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    create_date = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    chat_id = Column(String)
    favourite_team = Column(String)
    subscribe = Column(Boolean)
    create_date = Column(DateTime(timezone=True), server_default=func.now())


if __name__ == '__main__':
    Base.metadata.create_all(engine)
