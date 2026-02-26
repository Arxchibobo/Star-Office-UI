#!/bin/bash
# GitHub推送便捷脚本（使用环境变量）

cd ~/.openclaw/workspace

# 从环境变量或.github-token文件加载token
if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.openclaw/workspace/.github-token ]; then
        source ~/.openclaw/workspace/.github-token
    else
        echo "❌ GITHUB_TOKEN 未设置！"
        echo "请设置环境变量或创建 .github-token 文件"
        exit 1
    fi
fi

# 使用token推送
git push https://${GITHUB_TOKEN}@github.com/Arxchibobo/openclaw-arxchibo.git main

echo ""
echo "✅ 推送完成！"
