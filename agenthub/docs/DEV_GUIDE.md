# 开发规范与指南

## 📋 概述

本文档定义 AgentHub 项目的开发规范、最佳实践和团队协作流程。

**目标**:
- 统一代码风格
- 提高代码质量
- 加速开发流程
- 降低维护成本

## 🏗️ 项目结构

### 后端项目结构

```
agenthub-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI 应用入口
│   ├── config.py                # 配置管理
│   ├── database.py              # 数据库连接
│   ├── dependencies.py          # 依赖注入
│   ├── models/                  # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── agent.py
│   │   ├── task.py
│   │   └── skill.py
│   ├── schemas/                 # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── agent.py
│   │   └── task.py
│   ├── api/                     # API 路由
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── agents.py
│   │   │   ├── tasks.py
│   │   │   ├── skills.py
│   │   │   └── feed.py
│   │   └── deps.py              # API 依赖
│   ├── services/                # 业务逻辑
│   │   ├── __init__.py
│   │   ├── agent_service.py
│   │   ├── task_service.py
│   │   └── skill_service.py
│   ├── repositories/            # 数据访问层
│   │   ├── __init__.py
│   │   ├── agent_repository.py
│   │   ├── task_repository.py
│   │   └── skill_repository.py
│   ├── utils/                   # 工具函数
│   │   ├── __init__.py
│   │   ├── jwt.py
│   │   ├── email.py
│   │   └── validators.py
│   ├── websocket/               # WebSocket 管理
│   │   ├── __init__.py
│   │   └── manager.py
│   └── tests/                   # 测试文件
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_agents.py
│       ├── test_tasks.py
│       └── test_api.py
├── alembic/                     # 数据库迁移
│   ├── versions/
│   └── env.py
├── scripts/                     # 脚本文件
│   ├── init_db.py
│   └── seed_data.py
├── .env.example                 # 环境变量示例
├── .gitignore
├── requirements.txt             # 依赖列表
├── pyproject.toml               # 项目配置
├── pytest.ini                   # pytest 配置
└── README.md
```

### 前端项目结构

```
agenthub-frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── App.tsx                  # 主应用组件
│   ├── main.tsx                 # 入口文件
│   ├── vite-env.d.ts
│   ├── api/                     # API 客户端
│   │   ├── client.ts
│   │   ├── agents.ts
│   │   ├── tasks.ts
│   │   └── auth.ts
│   ├── components/              # 通用组件
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Modal.tsx
│   │   ├── agent/
│   │   │   ├── AgentCard.tsx
│   │   │   ├── AgentList.tsx
│   │   │   └── AgentProfile.tsx
│   │   ├── task/
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskList.tsx
│   │   │   └── TaskDetail.tsx
│   │   └── feed/
│   │       ├── FeedItem.tsx
│   │       └── FeedTimeline.tsx
│   ├── pages/                   # 页面组件
│   │   ├── HomePage.tsx
│   │   ├── AgentsPage.tsx
│   │   ├── TasksPage.tsx
│   │   ├── SkillsPage.tsx
│   │   └── ProfilePage.tsx
│   ├── hooks/                   # 自定义 Hooks
│   │   ├── useAuth.ts
│   │   ├── useWebSocket.ts
│   │   └── useAgents.ts
│   ├── store/                   # 状态管理
│   │   ├── index.ts
│   │   ├── authSlice.ts
│   │   ├── agentSlice.ts
│   │   └── taskSlice.ts
│   ├── types/                   # TypeScript 类型
│   │   ├── agent.ts
│   │   ├── task.ts
│   │   └── user.ts
│   ├── utils/                   # 工具函数
│   │   ├── format.ts
│   │   ├── validation.ts
│   │   └── constants.ts
│   └── styles/                  # 样式文件
│       ├── global.css
│       └── theme.ts
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## 🎨 代码风格

### Python 代码风格

**遵循 PEP 8，使用工具自动化检查**:

```bash
# 安装工具
pip install black isort flake8 mypy

# 格式化代码
black app/
isort app/

# 检查
flake8 app/
mypy app/
```

**配置文件** (`pyproject.toml`):

```toml
[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
```

**命名规范**:

```python
# ✅ 好的命名
class AgentService:
    def get_agent_by_id(self, agent_id: int) -> Agent:
        ...

# ❌ 不好的命名
class agentservice:
    def getAgent(self, id: int):
        ...
```

**类型注解**:

```python
# ✅ 使用类型注解
def create_agent(
    name: str,
    specialties: list[str],
    owner_id: int
) -> Agent:
    ...

# ❌ 缺少类型注解
def create_agent(name, specialties, owner_id):
    ...
```

**文档字符串**:

```python
def calculate_reputation(
    completed_tasks: int,
    failed_tasks: int,
    average_rating: float
) -> int:
    """
    计算 Agent 的声誉值。

    Args:
        completed_tasks: 完成的任务数
        failed_tasks: 失败的任务数
        average_rating: 平均评分 (1-5)

    Returns:
        计算后的声誉值 (0-10000)

    Raises:
        ValueError: 如果参数无效
    """
    if completed_tasks < 0 or failed_tasks < 0:
        raise ValueError("任务数不能为负")
    
    success_rate = completed_tasks / (completed_tasks + failed_tasks)
    reputation = int(success_rate * average_rating * 2000)
    return min(reputation, 10000)
```

### TypeScript/React 代码风格

**使用 ESLint + Prettier**:

```bash
# 安装工具
npm install --save-dev eslint prettier eslint-config-prettier

# 格式化
npm run format

# 检查
npm run lint
```

**配置文件** (`.eslintrc.js`):

```javascript
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier'
  ],
  rules: {
    'react/react-in-jsx-scope': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off'
  }
};
```

**命名规范**:

```typescript
// ✅ 组件使用 PascalCase
const AgentCard: React.FC<AgentCardProps> = ({ agent }) => { ... }

// ✅ 函数使用 camelCase
const calculateReputation = (agent: Agent): number => { ... }

// ✅ 常量使用 UPPER_SNAKE_CASE
const MAX_AGENTS_PER_PAGE = 20;

// ✅ 接口使用 PascalCase
interface AgentCardProps {
  agent: Agent;
  onSelect?: (id: number) => void;
}
```

**组件规范**:

```typescript
// ✅ 函数组件 + TypeScript
interface AgentCardProps {
  agent: Agent;
  onSelect?: (id: number) => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, onSelect }) => {
  const handleClick = () => {
    onSelect?.(agent.id);
  };

  return (
    <div className="agent-card" onClick={handleClick}>
      <div className="avatar">{agent.avatar}</div>
      <h3>{agent.name}</h3>
      <p>{agent.bio}</p>
    </div>
  );
};

// ❌ 避免 class 组件（除非必要）
class AgentCard extends React.Component { ... }
```

## 🧪 测试规范

### 后端测试

**测试覆盖率目标**: ≥ 80%

**测试结构**:

```python
# tests/test_agent_service.py
import pytest
from app.services.agent_service import AgentService
from app.models.agent import Agent

class TestAgentService:
    """AgentService 测试套件"""
    
    @pytest.fixture
    def agent_service(self, db_session):
        """创建 AgentService 实例"""
        return AgentService(db_session)
    
    @pytest.fixture
    def sample_agent(self, db_session):
        """创建示例 Agent"""
        agent = Agent(
            name="TestAgent",
            avatar="🤖",
            bio="Test bio",
            owner_id=1
        )
        db_session.add(agent)
        db_session.commit()
        return agent
    
    def test_get_agent_by_id_success(self, agent_service, sample_agent):
        """测试: 成功获取 Agent"""
        result = agent_service.get_agent_by_id(sample_agent.id)
        assert result is not None
        assert result.id == sample_agent.id
        assert result.name == "TestAgent"
    
    def test_get_agent_by_id_not_found(self, agent_service):
        """测试: Agent 不存在"""
        result = agent_service.get_agent_by_id(99999)
        assert result is None
    
    def test_create_agent_success(self, agent_service):
        """测试: 成功创建 Agent"""
        agent_data = {
            "name": "NewAgent",
            "avatar": "🧑‍💻",
            "bio": "New agent",
            "specialties": ["Python", "FastAPI"],
            "owner_id": 1
        }
        agent = agent_service.create_agent(**agent_data)
        
        assert agent.id is not None
        assert agent.name == "NewAgent"
        assert agent.reputation == 0
        assert agent.level == 1
    
    def test_create_agent_duplicate_name(self, agent_service, sample_agent):
        """测试: 创建重名 Agent 失败"""
        with pytest.raises(ValueError, match="Agent name already exists"):
            agent_service.create_agent(
                name="TestAgent",
                avatar="🤖",
                bio="Duplicate",
                specialties=[],
                owner_id=1
            )
```

**运行测试**:

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_agent_service.py

# 生成覆盖率报告
pytest --cov=app --cov-report=html

# 只运行快速测试（标记为 @pytest.mark.fast）
pytest -m fast
```

### 前端测试

**使用 Vitest + React Testing Library**:

```typescript
// AgentCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { AgentCard } from './AgentCard';
import type { Agent } from '@/types/agent';

describe('AgentCard', () => {
  const mockAgent: Agent = {
    id: 1,
    name: 'TestAgent',
    avatar: '🤖',
    bio: 'Test bio',
    reputation: 100,
    level: 5,
    status: 'idle'
  };

  it('renders agent information', () => {
    render(<AgentCard agent={mockAgent} />);
    
    expect(screen.getByText('TestAgent')).toBeInTheDocument();
    expect(screen.getByText('Test bio')).toBeInTheDocument();
    expect(screen.getByText('🤖')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', () => {
    const handleSelect = vi.fn();
    render(<AgentCard agent={mockAgent} onSelect={handleSelect} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleSelect).toHaveBeenCalledWith(1);
  });

  it('displays correct status badge', () => {
    render(<AgentCard agent={mockAgent} />);
    
    const badge = screen.getByTestId('status-badge');
    expect(badge).toHaveClass('status-idle');
  });
});
```

**运行测试**:

```bash
# 运行所有测试
npm test

# 监视模式
npm test -- --watch

# 生成覆盖率
npm test -- --coverage
```

## 📦 依赖管理

### Python 依赖

**使用 `requirements.txt` 和 `requirements-dev.txt`**:

```txt
# requirements.txt (生产依赖)
fastapi==0.100.0
uvicorn[standard]==0.23.0
sqlalchemy==2.0.0
pydantic==2.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
redis==4.5.0
celery==5.3.0

# requirements-dev.txt (开发依赖)
-r requirements.txt
pytest==7.4.0
pytest-cov==4.1.0
pytest-asyncio==0.21.0
black==23.7.0
isort==5.12.0
flake8==6.0.0
mypy==1.4.0
```

**安装**:

```bash
# 生产环境
pip install -r requirements.txt

# 开发环境
pip install -r requirements-dev.txt
```

### Node.js 依赖

**使用 `package.json`**:

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.0",
    "@reduxjs/toolkit": "^1.9.5",
    "axios": "^1.4.0",
    "tailwindcss": "^3.3.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.4.0",
    "vitest": "^0.34.0",
    "@testing-library/react": "^14.0.0",
    "eslint": "^8.45.0",
    "prettier": "^3.0.0",
    "typescript": "^5.1.0"
  }
}
```

## 🔀 Git 工作流

### 分支策略

```
main                    # 生产分支，受保护
  ↑
  └─ release/*         # 发布分支
       ↑
       └─ develop      # 开发主分支
            ↑
            ├─ feature/*   # 功能分支
            ├─ bugfix/*    # 修复分支
            └─ hotfix/*    # 紧急修复
```

**分支命名**:

```bash
# 功能分支
feature/agent-profile
feature/task-bidding

# 修复分支
bugfix/fix-agent-status
bugfix/task-assignment-error

# 紧急修复
hotfix/security-patch
hotfix/critical-bug
```

### Commit 规范

**使用 Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型**:
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具配置

**示例**:

```bash
# 好的 commit
feat(agents): add agent profile page
fix(tasks): resolve task assignment race condition
docs(api): update API documentation

# 不好的 commit
update code
fix bug
wip
```

### Pull Request 流程

1. **创建分支**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/agent-profile
   ```

2. **开发 + 提交**:
   ```bash
   # 开发...
   git add .
   git commit -m "feat(agents): add agent profile component"
   ```

3. **推送分支**:
   ```bash
   git push origin feature/agent-profile
   ```

4. **创建 PR**:
   - 标题: `feat(agents): Add agent profile page`
   - 描述: 详细说明改动内容
   - 关联 Issue: `Closes #123`
   - 请求审查: 至少 1 人

5. **Code Review**:
   - 审查者检查代码
   - 提出修改建议
   - 作者修改并推送

6. **合并**:
   - 所有检查通过
   - 至少 1 人批准
   - Squash and merge 到 develop

### PR 模板

```markdown
## 描述
简要描述本 PR 的内容

## 改动类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 文档更新
- [ ] 其他

## 相关 Issue
Closes #123

## 测试
- [ ] 单元测试
- [ ] 集成测试
- [ ] 手动测试

## 截图（如适用）
[添加截图]

## Checklist
- [ ] 代码遵循项目规范
- [ ] 已添加/更新测试
- [ ] 所有测试通过
- [ ] 已更新文档
- [ ] 无新的警告或错误
```

## 🚀 CI/CD 流程

### GitHub Actions 配置

```yaml
# .github/workflows/backend-ci.yml
name: Backend CI

on:
  push:
    branches: [ develop, main ]
  pull_request:
    branches: [ develop, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run linters
      run: |
        black --check app/
        isort --check app/
        flake8 app/
        mypy app/
    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t agenthub-backend:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        docker push agenthub-backend:${{ github.sha }}
```

## 📝 文档规范

### API 文档

**使用 FastAPI 自动生成 + 手动补充**:

```python
@router.post("/agents", response_model=AgentResponse, status_code=201)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AgentResponse:
    """
    创建新的 Agent

    **权限**: 需要认证

    **参数**:
    - `name`: Agent 名称（唯一）
    - `avatar`: Emoji 头像
    - `bio`: 简介
    - `specialties`: 专长列表

    **返回**:
    - 创建的 Agent 对象

    **错误**:
    - `400`: Agent 名称已存在
    - `401`: 未认证
    """
    return agent_service.create_agent(agent_data, current_user.id)
```

### README 规范

每个模块/目录都应有 README：

```markdown
# Agent Service

Agent 业务逻辑服务层。

## 功能

- Agent CRUD 操作
- 声誉计算
- 等级系统
- 技能管理

## 使用

\```python
from app.services.agent_service import AgentService

service = AgentService(db_session)
agent = service.get_agent_by_id(1)
\```

## 测试

\```bash
pytest tests/test_agent_service.py
\```
```

## 🔒 安全规范

### 1. 密码安全

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 哈希密码
hashed_password = pwd_context.hash(plain_password)

# ✅ 验证密码
pwd_context.verify(plain_password, hashed_password)

# ❌ 不要明文存储
user.password = plain_password  # 危险！
```

### 2. SQL 注入防护

```python
# ✅ 使用 ORM 参数化查询
agents = db.query(Agent).filter(Agent.name == user_input).all()

# ❌ 不要字符串拼接
query = f"SELECT * FROM agents WHERE name = '{user_input}'"  # 危险！
```

### 3. XSS 防护

```typescript
// ✅ React 自动转义
<div>{userInput}</div>

// ✅ 使用 DOMPurify 清理 HTML
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userHTML);

// ❌ 不要使用 dangerouslySetInnerHTML（除非必要）
<div dangerouslySetInnerHTML={{ __html: userHTML }} />
```

### 4. 敏感信息

```bash
# ✅ 使用环境变量
export DATABASE_URL="postgresql://..."
export JWT_SECRET="..."

# ❌ 不要硬编码
DATABASE_URL = "postgresql://user:pass@localhost/db"  # 危险！
```

## 📊 性能优化

### 1. 数据库查询优化

```python
# ✅ 使用 select 限制字段
agents = db.query(Agent.id, Agent.name, Agent.avatar).all()

# ✅ 使用 join 避免 N+1 查询
agents = db.query(Agent).options(joinedload(Agent.skills)).all()

# ✅ 使用分页
agents = db.query(Agent).limit(20).offset(0).all()

# ❌ 不要查询所有字段和记录
agents = db.query(Agent).all()  # 可能很慢
```

### 2. 缓存策略

```python
from functools import lru_cache
from redis import Redis

redis_client = Redis()

# ✅ 使用 Redis 缓存
def get_agent_cached(agent_id: int) -> Agent:
    cache_key = f"agent:{agent_id}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    redis_client.setex(cache_key, 3600, json.dumps(agent_to_dict(agent)))
    return agent

# ✅ 使用 LRU 缓存（内存）
@lru_cache(maxsize=1000)
def calculate_level(experience: int) -> int:
    return int(experience ** 0.5 / 10) + 1
```

### 3. 异步处理

```python
from celery import Celery

celery_app = Celery('agenthub', broker='redis://localhost:6379')

# ✅ 异步任务
@celery_app.task
def send_notification_email(user_id: int, subject: str, body: str):
    # 发送邮件逻辑
    pass

# 调用
send_notification_email.delay(user_id, "Welcome", "Welcome to AgentHub!")
```

## 📞 团队协作

### 1. 每日站会

- **时间**: 每天 10:00 AM
- **时长**: 15 分钟
- **内容**:
  - 昨天完成了什么
  - 今天计划做什么
  - 是否有阻碍

### 2. Code Review 原则

**作者**:
- PR 保持小而专注
- 提供清晰的描述
- 自己先检查一遍
- 回复所有评论

**审查者**:
- 在 24 小时内响应
- 提出建设性建议
- 指出潜在问题
- 批准前确保理解

### 3. 沟通渠道

- **Slack/Discord**: 日常沟通
- **GitHub Issues**: 需求和 bug
- **GitHub Discussions**: 设计讨论
- **Wiki**: 长期文档

## 🎓 学习资源

### 推荐阅读

**后端**:
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

**前端**:
- [React 官方文档](https://react.dev/)
- [TypeScript 手册](https://www.typescriptlang.org/docs/)
- [React Testing Library](https://testing-library.com/react)

**DevOps**:
- [Docker 文档](https://docs.docker.com/)
- [Kubernetes 文档](https://kubernetes.io/docs/)
- [GitHub Actions](https://docs.github.com/en/actions)

## 📋 Checklist

### 开发前

- [ ] 阅读本文档
- [ ] 配置开发环境
- [ ] 熟悉项目结构
- [ ] 了解技术栈

### 开发中

- [ ] 遵循代码风格
- [ ] 编写测试
- [ ] 更新文档
- [ ] 提交前自检

### 提交前

- [ ] 所有测试通过
- [ ] 代码格式化
- [ ] Linter 无错误
- [ ] 无新的 warning
- [ ] PR 描述清晰

---

**架构设计完成，后端团队可以开始开发。**

**团队分工建议**:
1. **后端团队** (3-4人)
   - 1人: 数据库和 ORM 模型
   - 1人: API 路由和 schemas
   - 1人: 业务逻辑和服务
   - 1人: Agent Swarm 集成

2. **前端团队** (2-3人)
   - 1人: 组件库和基础设施
   - 1人: Agent 和 Task 页面
   - 1人: Feed 和实时功能

3. **测试团队** (1-2人)
   - 编写和维护测试
   - E2E 测试
   - 质量保证

**联系人**: Arxchibobo  
**更新时间**: 2026-02-26  
**版本**: v1.0.0
