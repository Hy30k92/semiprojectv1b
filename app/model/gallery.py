from sqlalchemy import ForeignKey
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base

# 양방향 관계설정
class Gallery(Base):
    __tablename__ = 'gallery'

    gno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    userid: Mapped[str] = mapped_column(ForeignKey('member.userid'), index=True) # 비식별관계 -> 식별관계
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    views: Mapped[int] = mapped_column(default=0)
    contents: Mapped[str]
    attachs = relationship('GalAttach', back_populates='gallery') # 하나의 gallery 는 하나 이상의 attach 가 존재 ( 1:n )

class GalAttach(Base):
    __tablename__ = 'galattach'

    gano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    gno: Mapped[int] = mapped_column(ForeignKey('gallery.gno'), index=True)
    fname: Mapped[str] = mapped_column(nullable=False)
    fsize: Mapped[int] = mapped_column(default=0)
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    gallery = relationship('Gallery', back_populates='attachs') # 하나의 attach 는 하나의 gallery 에 속함 ( 1:1 )





