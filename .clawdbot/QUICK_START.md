# 🚀 Quick Start Guide

5分钟快速上手 Agent Swarm 系统。

## 步骤 1: 安装依赖

```bash
# 安装 jq
sudo apt install jq

# 安装 GitHub CLI
# 已安装 ✓

# 认证 GitHub CLI
gh auth login
# 选择: GitHub.com → HTTPS → Yes → Login with browser
```

## 步骤 2: 验证安装

```bash
cd ~/.openclaw/workspace
./swarm help
```

应该看到帮助信息。

## 步骤 3: 安装监控 Cron

```bash
./swarm install-cron
```

这会每10分钟自动检查所有 agent 的状态。

## 步骤 4: 创建第一个 Agent

```bash
./swarm spawn
```

**示例输入：**
```
Task ID: test-hello
Agent type: claude
Description: Create a test file
Prompt: (按 Ctrl+D 结束)
```

**Prompt 示例：**
```
Create a file called hello.js that prints "Hello, Agent Swarm!"

FILES TO CREATE:
- hello.js

CODE:
console.log("Hello, Agent Swarm!");

Test it by running: node hello.js
```

按 `Ctrl+D` 结束输入。

## 步骤 5: 监控 Agent

```bash
# 查看所有任务
./swarm status

# 查看日志
./swarm logs test-hello

# 实时查看（连接到 tmux）
./swarm attach test-hello
# 按 Ctrl+B 然后 D 退出
```

## 步骤 6: 中途干预（可选）

如果 agent 走错方向：

```bash
./swarm steer test-hello "Stop. Just create hello.js, don't do anything else."
```

## 步骤 7: 检查完成

几分钟后，运行：

```bash
./swarm status
```

应该看到任务状态更新。

## 步骤 8: 清理

```bash
./swarm cleanup
```

## 常见命令

```bash
# 查看帮助
./swarm help

# 查看状态
./swarm status

# 查看日志
./swarm logs <task-id>

# 连接到 agent
./swarm attach <task-id>

# 发送指令
./swarm steer <task-id> "your message"

# 杀死任务
./swarm kill <task-id>

# 清理完成的任务
./swarm cleanup

# 查看配置
./swarm config

# 手动触发检查
./swarm check
```

## 下一步

1. **阅读完整文档**
   ```bash
   cat ~/.openclaw/workspace/.clawdbot/README.md
   ```

2. **学习写好的 Prompt**
   ```bash
   cat ~/.openclaw/workspace/.clawdbot/PROMPT_TEMPLATES.md
   ```

3. **尝试真实任务**
   - 选择一个实际的 feature/bug
   - 写一个详细的 prompt
   - 生成 agent
   - 观察结果

## 故障排查

### Agent 没有启动

```bash
# 检查 tmux 会话
tmux ls

# 查看详细日志
cat ~/.openclaw/workspace/.clawdbot/logs/<task-id>.log
```

### GitHub CLI 问题

```bash
# 重新认证
gh auth login

# 测试
gh pr list
```

### Cron 没有运行

```bash
# 检查 cron 是否安装
crontab -l | grep check-agents

# 查看 cron 日志
tail -f ~/.openclaw/workspace/.clawdbot/logs/cron.log
```

## 进阶用法

### 批量创建 Agents

```bash
# 从任务列表文件
for task in billing templates dashboard; do
  ./swarm spawn <<EOF
feat-$task
codex
Implement $task feature
See PROMPT_TEMPLATES.md for structure
EOF
done
```

### 实时监控所有任务

```bash
watch -n 5 './swarm status'
```

### 查看所有日志

```bash
tail -f ~/.openclaw/workspace/.clawdbot/logs/*.log
```

---

**准备好了吗？**

```bash
cd ~/.openclaw/workspace
./swarm spawn
```

开始你的第一个 agent！🚀
