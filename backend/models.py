# sqlacodegen mysql+pymysql://<dbName>:<password>@localhost:<port>/<tableName> > models.py
# sqlacodegen mysql+pymysql://root:root@localhost:3306/event_everywhere > models.py

from typing import List, Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, aliased
import datetime
from database import Base

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func

# class Base(DeclarativeBase):
#     pass


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        Index('username', 'username', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255, 'utf8mb4_general_ci'))
    password: Mapped[str] = mapped_column(String(255, 'utf8mb4_general_ci'))
    name: Mapped[str] = mapped_column(String(255, 'utf8mb4_general_ci'))
    content: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))

    event: Mapped[List['Event']] = relationship('Event', back_populates='user')
    comment: Mapped[List['Comment']] = relationship('Comment', back_populates='user')
    like: Mapped[List['Like']] = relationship('Like', back_populates='user')


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL', name='event_ibfk_2'),
        Index('event_ibfk_1', 'root_id'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    root_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    title: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    category: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    img: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    content: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    start_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    end_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    latitude: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    longitude: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    address: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))

    user: Mapped[Optional['User']] = relationship('User', back_populates='event')
    comment: Mapped[List['Comment']] = relationship('Comment', back_populates='event')
    like: Mapped[List['Like']] = relationship('Like', back_populates='event')

    # related_count
    @hybrid_property
    def related_count(self):
        return getattr(self, "_related_count", None)

    @related_count.expression
    def related_count(cls):
        EventAlias = aliased(Event)
        return (
            select(func.count(EventAlias.id))
            .where(EventAlias.root_id == cls.root_id, EventAlias.id != cls.id)
            .correlate(cls)
            .scalar_subquery()
        )

    # like_count
    @hybrid_property
    def like_count(self):
        return len(self.like)

    @like_count.expression
    def like_count(cls):
        return (
            select(func.count(Like.id))
            .where(Like.event_id == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )

    # comment_count
    @hybrid_property
    def comment_count(self):
        return len(self.comment)

    @comment_count.expression
    def comment_count(cls):
        return (
            select(func.count(Comment.id))
            .where(Comment.event_id == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = (
        ForeignKeyConstraint(['event_id'], ['event.id'], ondelete='CASCADE', name='comment_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL', name='comment_ibfk_2'),
        Index('event_id', 'event_id'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    content: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_general_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    event: Mapped[Optional['Event']] = relationship('Event', back_populates='comment')
    user: Mapped[Optional['User']] = relationship('User', back_populates='comment')


class Like(Base):
    __tablename__ = 'like'
    __table_args__ = (
        ForeignKeyConstraint(['event_id'], ['event.id'], ondelete='CASCADE', name='like_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL', name='like_ibfk_2'),
        Index('event_id', 'event_id'),
        Index('user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    event: Mapped[Optional['Event']] = relationship('Event', back_populates='like')
    user: Mapped[Optional['User']] = relationship('User', back_populates='like')
