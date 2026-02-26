"""
Task 相关 API
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from database import get_db
from models import Task, Agent, User, TaskBid
from schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse,
    TaskBidCreate, TaskBidResponse, TaskAssign, TaskComplete,
    BidSummary
)
from auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建任务"""
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        requirements=task_data.requirements,
        reward_points=task_data.reward_points,
        difficulty=task_data.difficulty,
        category=task_data.category,
        created_by=current_user.id,
        deadline=task_data.deadline,
        estimated_hours=task_data.estimated_hours
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
    min_reward: Optional[int] = None,
    max_reward: Optional[int] = None,
    sort: str = Query("created_at", regex="^(reward_points|created_at|deadline)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """获取任务列表"""
    query = db.query(Task)
    
    # 过滤
    if status:
        query = query.filter(Task.status == status)
    if difficulty:
        query = query.filter(Task.difficulty == difficulty)
    if category:
        query = query.filter(Task.category == category)
    if min_reward:
        query = query.filter(Task.reward_points >= min_reward)
    if max_reward:
        query = query.filter(Task.reward_points <= max_reward)
    
    # 排序
    order_func = desc if order == "desc" else asc
    if sort == "reward_points":
        query = query.order_by(order_func(Task.reward_points))
    elif sort == "deadline":
        query = query.order_by(order_func(Task.deadline))
    else:
        query = query.order_by(order_func(Task.created_at))
    
    # 分页
    total = query.count()
    tasks = query.offset((page - 1) * limit).limit(limit).all()
    
    return tasks


@router.get("/{task_id}", response_model=TaskDetailResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """获取任务详情"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # 获取竞标信息
    bids = db.query(TaskBid).filter(TaskBid.task_id == task_id).all()
    bid_summaries = []
    for bid in bids:
        agent = db.query(Agent).filter(Agent.id == bid.agent_id).first()
        bid_summaries.append(BidSummary(
            id=bid.id,
            agent_id=bid.agent_id,
            agent_name=agent.name if agent else "Unknown",
            agent_avatar=agent.avatar if agent else "🤖",
            bid_message=bid.bid_message,
            estimated_time=bid.estimated_time,
            bid_points=bid.bid_points,
            status=bid.status,
            created_at=bid.created_at
        ))
    
    return {
        **task.__dict__,
        "creator": task.creator,
        "assigned_agent": task.assigned_agent,
        "bids": bid_summaries
    }


@router.post("/{task_id}/bids", response_model=TaskBidResponse, status_code=status.HTTP_201_CREATED)
def create_bid(
    task_id: int,
    bid_data: TaskBidCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Agent 竞标任务"""
    # 检查任务存在
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 检查任务是否可竞标
    if task.status != "open":
        raise HTTPException(status_code=400, detail="Task is not open for bidding")
    
    # 检查 Agent 存在且属于当前用户
    agent = db.query(Agent).filter(Agent.id == bid_data.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to bid with this agent")
    
    # 检查是否已竞标
    existing_bid = db.query(TaskBid).filter(
        TaskBid.task_id == task_id,
        TaskBid.agent_id == bid_data.agent_id
    ).first()
    if existing_bid:
        raise HTTPException(status_code=409, detail="Agent already bid on this task")
    
    # 创建竞标
    new_bid = TaskBid(
        task_id=task_id,
        agent_id=bid_data.agent_id,
        bid_message=bid_data.bid_message,
        estimated_time=bid_data.estimated_time,
        bid_points=bid_data.bid_points
    )
    
    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)
    
    return new_bid


@router.post("/{task_id}/assign", status_code=status.HTTP_200_OK)
def assign_task(
    task_id: int,
    assign_data: TaskAssign,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """分配任务给 Agent"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 权限检查：只有任务创建者可以分配
    if task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to assign this task")
    
    # 检查任务状态
    if task.status != "open":
        raise HTTPException(status_code=400, detail="Task is not open")
    
    # 检查 Agent 存在
    agent = db.query(Agent).filter(Agent.id == assign_data.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # 如果提供了 bid_id，验证 bid
    if assign_data.bid_id:
        bid = db.query(TaskBid).filter(
            TaskBid.id == assign_data.bid_id,
            TaskBid.task_id == task_id,
            TaskBid.agent_id == assign_data.agent_id
        ).first()
        if not bid:
            raise HTTPException(status_code=404, detail="Bid not found")
        bid.status = "accepted"
    
    # 分配任务
    task.assigned_agent_id = assign_data.agent_id
    task.status = "assigned"
    task.assigned_at = datetime.utcnow()
    
    # 更新 Agent 状态
    agent.status = "working"
    
    db.commit()
    
    return {
        "task_id": task_id,
        "agent_id": assign_data.agent_id,
        "status": "assigned",
        "assigned_at": task.assigned_at
    }


@router.post("/{task_id}/start", status_code=status.HTTP_200_OK)
def start_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """开始任务"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 检查 Agent 权限
    if not task.assigned_agent_id:
        raise HTTPException(status_code=400, detail="Task not assigned")
    
    agent = db.query(Agent).filter(Agent.id == task.assigned_agent_id).first()
    if agent.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # 检查任务状态
    if task.status != "assigned":
        raise HTTPException(status_code=400, detail="Task cannot be started")
    
    # 开始任务
    task.status = "in_progress"
    task.started_at = datetime.utcnow()
    agent.status = "working"
    
    db.commit()
    
    return {
        "task_id": task_id,
        "status": "in_progress",
        "started_at": task.started_at
    }


@router.post("/{task_id}/complete", status_code=status.HTTP_200_OK)
def complete_task(
    task_id: int,
    complete_data: TaskComplete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """完成任务"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 检查 Agent 权限
    if not task.assigned_agent_id:
        raise HTTPException(status_code=400, detail="Task not assigned")
    
    agent = db.query(Agent).filter(Agent.id == task.assigned_agent_id).first()
    if agent.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # 检查任务状态
    if task.status != "in_progress":
        raise HTTPException(status_code=400, detail="Task is not in progress")
    
    # 完成任务
    task.status = "completed"
    task.completed_at = datetime.utcnow()
    task.completion_notes = complete_data.completion_notes
    task.deliverables = complete_data.deliverables
    
    # 计算实际耗时
    if task.started_at:
        hours = (task.completed_at - task.started_at).total_seconds() / 3600
        task.actual_hours = round(hours, 2)
    
    # 更新 Agent 统计
    agent.total_tasks_completed += 1
    agent.experience_points += task.reward_points
    agent.reputation += 50  # 基础声誉奖励
    agent.status = "idle"
    
    # 计算等级（简单公式）
    agent.level = int((agent.experience_points / 100) ** 0.5) + 1
    
    # 给 Agent owner 发放奖励
    owner = db.query(User).filter(User.id == agent.owner_id).first()
    owner.points_balance += task.reward_points
    
    # 记录交易
    from models import Transaction
    transaction = Transaction(
        user_id=owner.id,
        agent_id=agent.id,
        transaction_type="task_reward",
        amount=task.reward_points,
        balance_after=owner.points_balance,
        description=f"Task completed: {task.title}",
        metadata={"task_id": task_id, "task_title": task.title}
    )
    db.add(transaction)
    
    db.commit()
    
    return {
        "task_id": task_id,
        "status": "completed",
        "completed_at": task.completed_at,
        "reward_points": task.reward_points,
        "agent_reputation_gain": 50
    }


@router.post("/{task_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_task(
    task_id: int,
    reason: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消任务"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 权限检查
    if task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this task")
    
    # 取消任务
    task.status = "cancelled"
    task.cancelled_at = datetime.utcnow()
    task.completion_notes = f"Cancelled: {reason}"
    
    # 释放 Agent
    if task.assigned_agent_id:
        agent = db.query(Agent).filter(Agent.id == task.assigned_agent_id).first()
        if agent:
            agent.status = "idle"
    
    db.commit()
    
    return {
        "task_id": task_id,
        "status": "cancelled",
        "reason": reason
    }
