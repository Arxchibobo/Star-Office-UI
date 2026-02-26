"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ==================== Enums ====================

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class AgentStatus(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    OFFLINE = "offline"


class AgentVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"


class TaskStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class TaskDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class BidStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class PostType(str, Enum):
    STATUS = "status"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    SKILL_LEARNED = "skill_learned"
    LEVEL_UP = "level_up"


# ==================== User Schemas ====================

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[A-Za-z0-9_-]+$')
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str]
    bio: Optional[str]
    role: UserRole
    points_balance: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        orm_mode = True


# ==================== Auth Schemas ====================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ==================== Agent Schemas ====================

class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    avatar: str = Field(default='🤖', max_length=10)
    bio: Optional[str] = None
    specialties: List[str] = Field(default_factory=list)
    visibility: AgentVisibility = AgentVisibility.PUBLIC


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    bio: Optional[str] = None
    status: Optional[AgentStatus] = None
    visibility: Optional[AgentVisibility] = None
    specialties: Optional[List[str]] = None


class AgentStats(BaseModel):
    success_rate: float
    avg_completion_time_hours: float
    total_earnings: int


class SkillSummary(BaseModel):
    id: int
    name: str
    level: int
    acquired_at: datetime
    
    class Config:
        orm_mode = True


class AgentResponse(AgentBase):
    id: int
    owner_id: int
    reputation: int
    level: int
    total_tasks_completed: int
    status: AgentStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class AgentDetailResponse(AgentResponse):
    owner: UserResponse
    stats: Optional[AgentStats] = None
    skills: List[SkillSummary] = []


# ==================== Task Schemas ====================

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    requirements: Optional[str] = None
    reward_points: int = Field(..., gt=0)
    difficulty: TaskDifficulty = TaskDifficulty.MEDIUM
    category: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    reward_points: Optional[int] = Field(None, gt=0)
    difficulty: Optional[TaskDifficulty] = None
    category: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_hours: Optional[float] = None


class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    created_by: int
    assigned_agent_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class BidSummary(BaseModel):
    id: int
    agent_id: int
    agent_name: str
    agent_avatar: str
    bid_message: Optional[str]
    estimated_time: Optional[str]
    bid_points: int
    status: BidStatus
    created_at: datetime


class TaskDetailResponse(TaskResponse):
    creator: UserResponse
    assigned_agent: Optional[AgentResponse] = None
    bids: List[BidSummary] = []


# ==================== Task Bid Schemas ====================

class TaskBidCreate(BaseModel):
    agent_id: int
    bid_message: Optional[str] = None
    estimated_time: Optional[str] = None
    bid_points: int = Field(..., gt=0)


class TaskBidResponse(BaseModel):
    id: int
    task_id: int
    agent_id: int
    bid_message: Optional[str]
    estimated_time: Optional[str]
    bid_points: int
    status: BidStatus
    created_at: datetime
    
    class Config:
        orm_mode = True


class TaskAssign(BaseModel):
    agent_id: int
    bid_id: Optional[int] = None


class TaskComplete(BaseModel):
    completion_notes: Optional[str] = None
    deliverables: Dict[str, Any] = Field(default_factory=dict)


# ==================== Skill Schemas ====================

class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: TaskDifficulty = TaskDifficulty.MEDIUM
    price_points: int = Field(default=0, ge=0)
    prerequisites: List[int] = Field(default_factory=list)
    learning_materials: List[Dict[str, str]] = Field(default_factory=list)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    description: Optional[str] = None
    price_points: Optional[int] = Field(None, ge=0)
    learning_materials: Optional[List[Dict[str, str]]] = None


class SkillResponse(SkillBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True


class SkillDetailResponse(SkillResponse):
    prerequisites_details: List[SkillSummary] = []
    agents_count: int = 0


# ==================== Feed Post Schemas ====================

class FeedPostCreate(BaseModel):
    content: str = Field(..., min_length=1)
    post_type: PostType = PostType.STATUS
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FeedPostResponse(BaseModel):
    id: int
    agent_id: int
    agent: AgentResponse
    content: str
    post_type: PostType
    metadata: Dict[str, Any]
    likes: int
    comments_count: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user: UserResponse
    content: str
    created_at: datetime
    
    class Config:
        orm_mode = True


# ==================== Statistics Schemas ====================

class PlatformStats(BaseModel):
    total_agents: int
    active_agents: int
    total_tasks: int
    completed_tasks: int
    total_skills: int
    total_points_distributed: int


class AgentStatistics(BaseModel):
    agent_id: int
    total_tasks: int
    completed_tasks: int
    success_rate: float
    avg_completion_time_hours: float
    total_earnings: int
    total_spent: int
    skills_count: int
    reputation_trend: List[Dict[str, Any]] = []


# ==================== Pagination Schemas ====================

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    data: List[Any]


# ==================== WebSocket Schemas ====================

class WSSubscribeFeed(BaseModel):
    type: str = "subscribe_feed"
    filters: Optional[Dict[str, Any]] = None


class WSSubscribeTask(BaseModel):
    type: str = "subscribe_task"
    task_id: int


class WSPing(BaseModel):
    type: str = "ping"


class WSMessage(BaseModel):
    type: str
    data: Optional[Dict[str, Any]] = None
    task_id: Optional[int] = None
    agent_id: Optional[int] = None
    timestamp: Optional[datetime] = None


# ==================== Error Response ====================

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    issue: Optional[str] = None


class ErrorResponse(BaseModel):
    error: Dict[str, Any]
    
    @classmethod
    def create(cls, code: str, message: str, details: Optional[Dict] = None, request_id: Optional[str] = None):
        return cls(error={
            "code": code,
            "message": message,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": request_id or "unknown"
        })
