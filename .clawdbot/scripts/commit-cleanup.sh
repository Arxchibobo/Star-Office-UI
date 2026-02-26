#!/bin/bash
# 🧹 Workspace Cleanup - Git Commit Helper
# Generated: 2026-02-26 13:44 GMT+8

echo "🧹 OpenClaw Workspace Cleanup - Git Commit Helper"
echo "=================================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "WORKSPACE_REPORT.md" ]; then
    echo "❌ Error: Must run from workspace root"
    exit 1
fi

echo "📊 Changes Summary:"
echo "-------------------"
git status --short | head -20
echo ""
echo "... and more"
echo ""

echo "⚠️  Submodule Notice:"
echo "---------------------"
echo "The following projects have independent .git directories:"
echo "  - projects/clawproduct-hunt/"
echo "  - projects/telegram-subagent-hooks/"
echo ""
echo "These should be converted to git submodules later."
echo ""

echo "📝 Suggested Commit Message:"
echo "----------------------------"
cat << 'EOF'
🧹 Workspace cleanup and reorganization

Major structural improvements to workspace organization:

## 📁 Directory Structure
- Created logical hierarchy (assets/, projects/, docs/)
- Archived images to assets/images/ (18MB)
- Moved subprojects to projects/
- Organized old docs to docs/archived/

## 🔧 Configuration
- Enhanced .gitignore (37 → 95 lines, 6 categories)
- Verified Agent Swarm system integrity
- Consolidated scripts to .clawdbot/scripts/

## 📦 Projects
- Moved clawproduct-hunt/ to projects/
- Moved telegram-subagent-hooks/ to projects/
- Archived demo-video/ to projects/archived/ (406M)

## 📚 Documentation
- Added WORKSPACE_REPORT.md (comprehensive cleanup report)
- Added PROJECTS.md (project overview)
- Moved project-arch/ to agenthub/docs/
- Archived bobo_notes/ to docs/archived/

## ✅ Benefits
- Improved maintainability
- Clear separation of concerns
- Better navigation
- Enhanced Git hygiene
- Space management (~380M optimizable)

See WORKSPACE_REPORT.md for detailed analysis.

Files changed: 88+
Workspace size: ~878M
Optimizable: ~380M (demo-video dependencies)
EOF
echo ""
echo "----------------------------"
echo ""

echo "🚀 Next Steps:"
echo "-------------"
echo "1. Review changes: git diff --stat"
echo "2. Commit changes: git commit -F <(bash $0 commit-message)"
echo "3. Push to remote: git push"
echo "4. Convert subprojects to submodules (optional)"
echo "5. Clean up demo-video node_modules to save 380M"
echo ""

echo "💡 Quick Actions:"
echo "-----------------"
echo "# Commit with suggested message"
echo "git commit -m \"\$(bash $0 commit-message | tail -n +13 | head -n -15)\""
echo ""
echo "# Clean up space"
echo "rm -rf projects/archived/demo-video/node_modules/"
echo "rm -rf projects/archived/demo-video/out/"
echo ""

exit 0
