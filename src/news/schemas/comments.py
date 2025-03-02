"""
Comment schema
"""

from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class CommentReadSchema(BaseModel):

    id: int
    text: str
    created: datetime
    updated: datetime
    user_id: UUID

    class Config:
        from_attributes = True

class CommentCreateSchema(BaseModel):
    text: str
    news_id: int