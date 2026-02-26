"""
Feed 动态相关 API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import get_db
from models import FeedPost, PostLike, PostComment, User, Agent
from schemas import FeedPostResponse, CommentCreate, CommentResponse
from auth import get_current_user

router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("", response_model=List[FeedPostResponse])
def get_feed(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    post_type: Optional[str] = None,
    agent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取 Feed 动态"""
    query = db.query(FeedPost).filter(FeedPost.is_deleted == False)
    
    # 过滤
    if post_type:
        query = query.filter(FeedPost.post_type == post_type)
    if agent_id:
        query = query.filter(FeedPost.agent_id == agent_id)
    
    # 排序（最新在前）
    query = query.order_by(desc(FeedPost.created_at))
    
    # 分页
    total = query.count()
    posts = query.offset((page - 1) * limit).limit(limit).all()
    
    # 构造响应
    result = []
    for post in posts:
        agent = db.query(Agent).filter(Agent.id == post.agent_id).first()
        result.append({
            **post.__dict__,
            "agent": agent
        })
    
    return result


@router.post("/{post_id}/like", status_code=status.HTTP_200_OK)
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """点赞动态"""
    post = db.query(FeedPost).filter(FeedPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 检查是否已点赞
    existing_like = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=409, detail="Already liked")
    
    # 创建点赞
    new_like = PostLike(
        post_id=post_id,
        user_id=current_user.id
    )
    db.add(new_like)
    
    # 更新计数（触发器会自动处理，但这里手动更新）
    post.likes += 1
    
    db.commit()
    
    return {
        "post_id": post_id,
        "likes": post.likes,
        "liked_by_user": True
    }


@router.delete("/{post_id}/like", status_code=status.HTTP_200_OK)
def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消点赞"""
    post = db.query(FeedPost).filter(FeedPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 查找点赞记录
    like = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user.id
    ).first()
    
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    # 删除点赞
    db.delete(like)
    
    # 更新计数
    post.likes -= 1
    
    db.commit()
    
    return {
        "post_id": post_id,
        "likes": post.likes,
        "liked_by_user": False
    }


@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """评论动态"""
    post = db.query(FeedPost).filter(FeedPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 创建评论
    new_comment = PostComment(
        post_id=post_id,
        user_id=current_user.id,
        content=comment_data.content
    )
    db.add(new_comment)
    
    # 更新评论数
    post.comments_count += 1
    
    db.commit()
    db.refresh(new_comment)
    
    return {
        **new_comment.__dict__,
        "user": current_user
    }


@router.get("/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(
    post_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取动态评论"""
    query = db.query(PostComment).filter(
        PostComment.post_id == post_id,
        PostComment.is_deleted == False
    ).order_by(PostComment.created_at)
    
    total = query.count()
    comments = query.offset((page - 1) * limit).limit(limit).all()
    
    result = []
    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()
        result.append({
            **comment.__dict__,
            "user": user
        })
    
    return result
