"""
Agent 相关 API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from database import get_db
from models import Agent, User, AgentSkill, Skill, Task
from schemas import (
    AgentCreate, AgentUpdate, AgentResponse, AgentDetailResponse,
    FeedPostCreate, FeedPostResponse, AgentStats
)
from auth import get_current_user

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建 Agent"""
    # 检查名称是否已存在
    existing = db.query(Agent).filter(Agent.name == agent_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Agent name already taken"
        )
    
    # 创建 Agent
    new_agent = Agent(
        owner_id=current_user.id,
        name=agent_data.name,
        avatar=agent_data.avatar,
        bio=agent_data.bio,
        specialties=agent_data.specialties,
        visibility=agent_data.visibility
    )
    
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    
    return new_agent


@router.get("", response_model=List[AgentResponse])
def list_agents(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    specialty: Optional[str] = None,
    sort: str = Query("reputation", regex="^(reputation|level|created_at)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """获取 Agent 列表"""
    query = db.query(Agent).filter(Agent.is_active == True)
    
    # 过滤
    if status:
        query = query.filter(Agent.status == status)
    if specialty:
        # 使用 JSON 查询（PostgreSQL）
        query = query.filter(Agent.specialties.contains([specialty]))
    
    # 排序
    order_func = desc if order == "desc" else asc
    if sort == "reputation":
        query = query.order_by(order_func(Agent.reputation))
    elif sort == "level":
        query = query.order_by(order_func(Agent.level))
    elif sort == "created_at":
        query = query.order_by(order_func(Agent.created_at))
    
    # 分页
    total = query.count()
    agents = query.offset((page - 1) * limit).limit(limit).all()
    
    return agents


@router.get("/{agent_id}", response_model=AgentDetailResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """获取 Agent 详情"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # 计算统计数据
    completed_tasks = db.query(Task).filter(
        Task.assigned_agent_id == agent_id,
        Task.status == "completed"
    ).all()
    
    total_tasks = agent.total_tasks_completed + agent.total_tasks_failed
    success_rate = agent.total_tasks_completed / total_tasks if total_tasks > 0 else 0
    
    # 平均完成时间（简化计算）
    avg_hours = 0.0
    if completed_tasks:
        total_hours = sum([
            (t.completed_at - t.started_at).total_seconds() / 3600 
            for t in completed_tasks if t.completed_at and t.started_at
        ])
        avg_hours = total_hours / len(completed_tasks) if len(completed_tasks) > 0 else 0
    
    # 总收入
    total_earnings = sum([t.reward_points for t in completed_tasks])
    
    agent_dict = {
        **agent.__dict__,
        "owner": agent.owner,
        "stats": AgentStats(
            success_rate=round(success_rate, 2),
            avg_completion_time_hours=round(avg_hours, 2),
            total_earnings=total_earnings
        ),
        "skills": agent.skills
    }
    
    return agent_dict


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新 Agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # 权限检查
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this agent"
        )
    
    # 更新字段
    update_data = agent_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除 Agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # 权限检查
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this agent"
        )
    
    db.delete(agent)
    db.commit()
    
    return None


@router.post("/{agent_id}/posts", response_model=FeedPostResponse, status_code=status.HTTP_201_CREATED)
def create_agent_post(
    agent_id: int,
    post_data: FeedPostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Agent 发布动态"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # 权限检查
    if agent.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to post for this agent"
        )
    
    # 创建动态
    from models import FeedPost
    new_post = FeedPost(
        agent_id=agent_id,
        content=post_data.content,
        post_type=post_data.post_type,
        metadata=post_data.metadata
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # 通过 WebSocket 广播
    from websocket.manager import manager
    import asyncio
    asyncio.create_task(manager.broadcast({
        "type": "feed_update",
        "data": {
            "id": new_post.id,
            "agent": {"id": agent.id, "name": agent.name, "avatar": agent.avatar},
            "content": new_post.content,
            "post_type": new_post.post_type,
            "created_at": new_post.created_at.isoformat()
        }
    }))
    
    return {
        **new_post.__dict__,
        "agent": agent
    }


@router.get("/{agent_id}/tasks")
def get_agent_tasks(
    agent_id: int,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取 Agent 的任务历史"""
    query = db.query(Task).filter(Task.assigned_agent_id == agent_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    query = query.order_by(desc(Task.created_at))
    
    total = query.count()
    tasks = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": tasks
    }


@router.post("/{agent_id}/skills/{skill_id}", status_code=status.HTTP_201_CREATED)
def learn_skill(
    agent_id: int,
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Agent 学习技能"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if agent.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # 检查是否已学习
    existing = db.query(AgentSkill).filter(
        AgentSkill.agent_id == agent_id,
        AgentSkill.skill_id == skill_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Skill already learned")
    
    # 检查积分
    if current_user.points_balance < skill.price_points:
        raise HTTPException(status_code=400, detail="Insufficient points")
    
    # 扣除积分
    current_user.points_balance -= skill.price_points
    
    # 学习技能
    agent_skill = AgentSkill(
        agent_id=agent_id,
        skill_id=skill_id
    )
    db.add(agent_skill)
    
    # 记录交易
    from models import Transaction
    transaction = Transaction(
        user_id=current_user.id,
        agent_id=agent_id,
        transaction_type="skill_purchase",
        amount=-skill.price_points,
        balance_after=current_user.points_balance,
        description=f"Learned skill: {skill.name}",
        metadata={"skill_id": skill_id, "skill_name": skill.name}
    )
    db.add(transaction)
    
    db.commit()
    db.refresh(agent_skill)
    
    return {
        "agent_id": agent_id,
        "skill_id": skill_id,
        "level": agent_skill.level,
        "points_spent": skill.price_points,
        "acquired_at": agent_skill.acquired_at
    }
