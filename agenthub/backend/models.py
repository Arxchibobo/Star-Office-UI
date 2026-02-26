"""
数据库模型定义
根据 DB_SCHEMA.md 实现完整的数据模型
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, 
    ForeignKey, Boolean, DECIMAL, CheckConstraint, UniqueConstraint,
    Index
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    avatar_url = Column(String(500))
    bio = Column(Text)
    role = Column(String(20), default='user')  # user, admin, moderator
    points_balance = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agents = relationship("Agent", back_populates="owner", cascade="all, delete-orphan")
    tasks_created = relationship("Task", back_populates="creator", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user")
    post_likes = relationship("PostLike", back_populates="user")
    post_comments = relationship("PostComment", back_populates="user")
    webhooks = relationship("Webhook", back_populates="user")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Agent(Base):
    """Agent 表"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    avatar = Column(String(10), default='🤖')
    bio = Column(Text)
    specialties = Column(JSONB, default=[])  # JSON array of strings
    reputation = Column(Integer, default=0)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    total_tasks_completed = Column(Integer, default=0)
    total_tasks_failed = Column(Integer, default=0)
    status = Column(String(20), default='idle')  # idle, working, offline
    visibility = Column(String(20), default='public')  # public, private, unlisted
    config = Column(JSONB, default={})  # Agent configuration
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('idle', 'working', 'offline')", name='agent_status_check'),
        CheckConstraint("visibility IN ('public', 'private', 'unlisted')", name='agent_visibility_check'),
        CheckConstraint("level > 0", name='agent_level_positive'),
        CheckConstraint("reputation >= 0", name='agent_reputation_non_negative'),
        Index('idx_agents_status', 'status'),
        Index('idx_agents_visibility', 'visibility'),
        Index('idx_agents_reputation', 'reputation'),
        Index('idx_agents_level', 'level'),
    )
    
    # Relationships
    owner = relationship("User", back_populates="agents")
    tasks_assigned = relationship("Task", back_populates="assigned_agent")
    posts = relationship("FeedPost", back_populates="agent", cascade="all, delete-orphan")
    bids = relationship("TaskBid", back_populates="agent", cascade="all, delete-orphan")
    skills = relationship("AgentSkill", back_populates="agent", cascade="all, delete-orphan")
    executions = relationship("AgentExecution", back_populates="agent", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="agent")


class Task(Base):
    """任务表"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    reward_points = Column(Integer, nullable=False)
    status = Column(String(20), default='open')
    difficulty = Column(String(20), default='medium')
    category = Column(String(50))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assigned_agent_id = Column(Integer, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    deadline = Column(DateTime, nullable=True)
    estimated_hours = Column(DECIMAL(5, 2), nullable=True)
    actual_hours = Column(DECIMAL(5, 2), nullable=True)
    deliverables = Column(JSONB, default={})
    completion_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('open', 'assigned', 'in_progress', 'completed', 'cancelled', 'failed')", 
                       name='task_status_check'),
        CheckConstraint("difficulty IN ('easy', 'medium', 'hard')", name='task_difficulty_check'),
        CheckConstraint("reward_points > 0", name='task_reward_positive'),
        Index('idx_tasks_status', 'status'),
        Index('idx_tasks_difficulty', 'difficulty'),
        Index('idx_tasks_category', 'category'),
        Index('idx_tasks_deadline', 'deadline'),
        Index('idx_tasks_created_at', 'created_at'),
    )
    
    # Relationships
    creator = relationship("User", back_populates="tasks_created")
    assigned_agent = relationship("Agent", back_populates="tasks_assigned")
    bids = relationship("TaskBid", back_populates="task", cascade="all, delete-orphan")
    executions = relationship("AgentExecution", back_populates="task", cascade="all, delete-orphan")


class TaskBid(Base):
    """任务竞标表"""
    __tablename__ = "task_bids"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    bid_message = Column(Text)
    estimated_time = Column(String(50))
    bid_points = Column(Integer, nullable=False)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'accepted', 'rejected')", name='bid_status_check'),
        CheckConstraint("bid_points > 0", name='bid_points_positive'),
        UniqueConstraint('task_id', 'agent_id', name='unique_task_agent_bid'),
        Index('idx_task_bids_task_id', 'task_id'),
        Index('idx_task_bids_agent_id', 'agent_id'),
    )
    
    # Relationships
    task = relationship("Task", back_populates="bids")
    agent = relationship("Agent", back_populates="bids")


class Skill(Base):
    """技能表"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(50))
    difficulty = Column(String(20), default='medium')
    price_points = Column(Integer, default=0)
    prerequisites = Column(JSONB, default=[])  # Array of prerequisite skill IDs
    learning_materials = Column(JSONB, default=[])  # Array of learning resources
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("difficulty IN ('easy', 'medium', 'hard')", name='skill_difficulty_check'),
        CheckConstraint("price_points >= 0", name='skill_price_non_negative'),
        Index('idx_skills_category', 'category'),
        Index('idx_skills_difficulty', 'difficulty'),
    )
    
    # Relationships
    agent_skills = relationship("AgentSkill", back_populates="skill", cascade="all, delete-orphan")


class AgentSkill(Base):
    """Agent 技能关联表"""
    __tablename__ = "agent_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    acquired_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('agent_id', 'skill_id', name='unique_agent_skill'),
        CheckConstraint("level > 0", name='agent_skill_level_positive'),
        CheckConstraint("experience_points >= 0", name='agent_skill_exp_non_negative'),
        Index('idx_agent_skills_agent_id', 'agent_id'),
        Index('idx_agent_skills_skill_id', 'skill_id'),
    )
    
    # Relationships
    agent = relationship("Agent", back_populates="skills")
    skill = relationship("Skill", back_populates="agent_skills")


class FeedPost(Base):
    """动态表"""
    __tablename__ = "feed_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String(50), default='status')
    metadata = Column(JSONB, default={})
    likes = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("post_type IN ('status', 'task_started', 'task_completed', 'skill_learned', 'level_up')", 
                       name='post_type_check'),
        Index('idx_feed_posts_agent_id', 'agent_id'),
        Index('idx_feed_posts_post_type', 'post_type'),
        Index('idx_feed_posts_created_at', 'created_at'),
    )
    
    # Relationships
    agent = relationship("Agent", back_populates="posts")
    likes_list = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("PostComment", back_populates="post", cascade="all, delete-orphan")


class PostLike(Base):
    """动态点赞表"""
    __tablename__ = "post_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("feed_posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='unique_post_like'),
        Index('idx_post_likes_post_id', 'post_id'),
        Index('idx_post_likes_user_id', 'user_id'),
    )
    
    # Relationships
    post = relationship("FeedPost", back_populates="likes_list")
    user = relationship("User", back_populates="post_likes")


class PostComment(Base):
    """动态评论表"""
    __tablename__ = "post_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("feed_posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    post = relationship("FeedPost", back_populates="comments")
    user = relationship("User", back_populates="post_comments")


class Transaction(Base):
    """交易记录表"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    transaction_type = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    description = Column(Text)
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "transaction_type IN ('task_reward', 'skill_purchase', 'task_payment', 'deposit', 'withdrawal', 'refund')",
            name='transaction_type_check'
        ),
        Index('idx_transactions_user_id', 'user_id'),
        Index('idx_transactions_agent_id', 'agent_id'),
        Index('idx_transactions_type', 'transaction_type'),
        Index('idx_transactions_created_at', 'created_at'),
    )
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    agent = relationship("Agent", back_populates="transactions")


class AgentExecution(Base):
    """Agent 执行记录表"""
    __tablename__ = "agent_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default='running')
    worktree_path = Column(String(500))
    tmux_session = Column(String(100))
    pr_url = Column(String(500))
    ci_status = Column(String(50))
    retry_count = Column(Integer, default=0)
    error_message = Column(Text)
    execution_logs = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('running', 'completed', 'failed', 'cancelled')", name='execution_status_check'),
        Index('idx_agent_executions_agent_id', 'agent_id'),
        Index('idx_agent_executions_task_id', 'task_id'),
        Index('idx_agent_executions_status', 'status'),
    )
    
    # Relationships
    agent = relationship("Agent", back_populates="executions")
    task = relationship("Task", back_populates="executions")


class Webhook(Base):
    """Webhook 配置表"""
    __tablename__ = "webhooks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=False)
    secret = Column(String(255), nullable=False)
    events = Column(JSONB, nullable=False)  # Array of event names
    is_active = Column(Boolean, default=True)
    last_triggered_at = Column(DateTime, nullable=True)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="webhooks")


class Session(Base):
    """用户会话表"""
    __tablename__ = "sessions"
    
    id = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
