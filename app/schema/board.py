from typing import Optional

from pydantic import BaseModel, Field


class Board(BaseModel):
    title: str
    userid: str
    contents: str
    # captcha: str

class NewReply(BaseModel):
    reply: str
    userid: str
    bno: int
    rppno: Optional[int] = Field(default=None) # 선택사항

