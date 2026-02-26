"""
AgentHub - AI Agent Social Platform & Skill Marketplace
主应用入口
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
import time

from database import init_db
from websocket.manager import manager
from schemas import ErrorResponse

# 导入所有 API 路由
from api import auth, agents, tasks, feed

# 创建 FastAPI 应用
app = FastAPI(
    title="AgentHub API",
    description="AI Agent Social Platform & Skill Marketplace - Complete RESTful API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==================== 中间件 ====================

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    print(f"❌ Unhandled exception: {exc}")
    error_response = ErrorResponse.create(
        code="INTERNAL_ERROR",
        message="An unexpected error occurred",
        details={"error": str(exc)},
        request_id=str(id(request))
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


# ==================== 注册路由 ====================

app.include_router(auth.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(feed.router, prefix="/api")


# ==================== WebSocket ====================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 端点用于实时通信"""
    await manager.connect(websocket)
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_json()
            
            # 处理不同类型的消息
            msg_type = data.get("type")
            if msg_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": time.time()
                })
            elif msg_type == "subscribe_feed":
                # 实现订阅逻辑
                pass
            elif msg_type == "subscribe_task":
                # 实现任务订阅
                pass
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("WebSocket client disconnected")


# ==================== 静态文件和根路由 ====================

# 挂载静态文件（前端）
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
async def root():
    """根路径 - 返回 API 信息"""
    return {
        "service": "AgentHub API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health():
    """健康检查端点"""
    return {
        "status": "ok",
        "service": "AgentHub",
        "version": "1.0.0"
    }


# ==================== 启动事件 ====================

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("="*60)
    print("🚀 AgentHub API Server Starting...")
    print("="*60)
    
    # 初始化数据库
    init_db()
    
    print("✅ Database initialized")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("="*60)


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("🛑 AgentHub API Server Shutting Down...")


# ==================== 主程序入口 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False  # 生产环境设为 False
    )
