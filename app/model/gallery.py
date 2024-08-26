from sqlalchemy import ForeignKey
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class gallery(Base):
    __tablename__ = 'gallery'

    gno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    userid: Mapped[str] = mapped_column(ForeignKey('member.userid'), index=True) # 비식별관계 -> 식별관계
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)
    views: Mapped[int] = mapped_column(default=0)
    contents: Mapped[str]

class GalAttach(Base):
    __tablename__ = 'galattach'

    gano: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    gno: Mapped[int] = mapped_column(ForeignKey('gallery.gno'), index=True)
    fname: Mapped[str] = mapped_column(nullable=False)
    fsuze: Mapped[int] = mapped_column(default=0)
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)







