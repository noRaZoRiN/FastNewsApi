from typing import Sequence, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi_users.authentication import Authenticator

from src.users.models import User
from src.users.routers import fastapi_users
from src import get_db
from ..models import Comment
from ..schemas import CommentReadSchema, CommentCreateSchema
from ..services import CommentService

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)



@router.get("/{news_id}", response_model=List[CommentReadSchema])
async def get_comments(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
) -> Sequence[Comment]:
    return await CommentService.get_comments(db=db, news_id=news_id, offset=offset, limit=limit)


@router.get("/{comment_id}", response_model=CommentReadSchema)
async def get_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
) -> Comment:
    return await CommentService.get_comment(db=db, comment_id=comment_id)


@router.post("", response_model=CommentCreateSchema)
async def create_comment(
    comment: CommentCreateSchema,
    current_user: User = Depends(fastapi_users.current_user(active=True)),
    db: AsyncSession = Depends(get_db),
) -> Comment:
    comment_data = comment.dict()
    return await CommentService.create_comment(db=db, comment_data=comment_data, user=current_user)

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fastapi_users.current_user(active=True)),
) -> dict:
    await CommentService.delete_comment(db=db, comment_id=comment_id, user=current_user)
    return {"detail": "Comment deleted"}

@router.put("/{comment_id}", response_model=CommentReadSchema)
async def update_comment(
    comment_id: int,
    comment: CommentCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fastapi_users.current_user(active=True)),
) -> Comment:
    comment_data = comment.dict()
    return await CommentService.update_comment(db=db, comment_id=comment_id, comment_data=comment_data, user=current_user)


@router.patch("/{comment_id}", response_model=CommentReadSchema)
async def partial_update_comment(
    comment_id: int,
    comment: CommentCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fastapi_users.current_user(active=True)),
) -> Comment:
    comment_data = comment.dict()
    return await CommentService.partial_update_comment(db=db, comment_id=comment_id, comment_data=comment_data, user=current_user)