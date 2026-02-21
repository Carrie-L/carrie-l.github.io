#!/usr/bin/env bash
# novel_orchestrator.sh - 主 Agent 用来管理子 Agent 写小说的脚本
# 用法: ./novel_orchestrator.sh <command>
# 命令: start | review | push | continue

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$SCRIPT_DIR/.."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 获取下一个待写章节
get_next_chapter() {
    cd "$WORKSPACE"
    # 找到第一个 - [ ] 章节
    local chapter=$(grep -m1 '^- \[ \] `' AndroidDeveloperGuideStory/Contents/00-目录.md | sed 's/^- \[ \] `\(.*\)`.*/\1/')
    echo "$chapter"
}

# 启动子 Agent 写小说
cmd_start() {
    local chapter=$(get_next_chapter)
    if [ -z "$chapter" ]; then
        log_error "没有找到待写的章节"
        exit 1
    fi

    log_info "开始写章节: $chapter"
    log_info "使用 prompt: $SCRIPT_DIR/novel-writer-prompt.md"

    # TODO: 实际调用 sessions_spawn
    # sessions_spawn --agent novel-writer --task "请写章节 $chapter"

    echo ""
    echo "========================================"
    echo "请手动执行以下命令启动子 Agent："
    echo "========================================"
    echo "subagents spawn --task \"请读取 $SCRIPT_DIR/novel-writer-prompt.md 并开始工作\""
}

# 审查章节
cmd_review() {
    log_info "请检查章节质量..."

    # 检查最新的 commit
    cd "$WORKSPACE"
    local latest_commit=$(git log -1 --oneline)
    log_info "最新 commit: $latest_commit"

    # TODO: 实际调用审查逻辑
    echo ""
    echo "请人工审查以下内容："
    echo "1. 章节内容是否与官方文档对齐"
    echo "2. 写作风格是否符合要求"
    echo "3. 门禁是否通过"
    echo ""
    echo "审查结果："
    echo "  - 通过: 输入 'push' 继续"
    echo "  - 需修改: 输入 'fix' 让子 Agent 修正"
}

# 推送章节
cmd_push() {
    cd "$WORKSPACE"
    log_info "推送章节到远程仓库..."
    git push
    log_info "推送成功！"
}

# 显示帮助
cmd_help() {
    echo "小说写作编排脚本"
    echo ""
    echo "用法: $0 <command>"
    echo ""
    echo "命令:"
    echo "  start   - 启动子 Agent 写下一章"
    echo "  review  - 审查最新章节"
    echo "  push    - 推送通过审查的章节"
    echo "  help    - 显示帮助"
    echo ""
    echo "完整流程:"
    echo "  $0 start   # 子 Agent 写章节"
    echo "  $0 review  # 主 Agent 审查"
    echo "  # (如果需要修改，输入 fix)"
    echo "  $0 push    # 推送到远程"
    echo "  $0 start   # 继续下一章..."
}

# 主入口
case "$1" in
    start)
        cmd_start
        ;;
    review)
        cmd_review
        ;;
    push)
        cmd_push
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        log_error "未知命令: $1"
        cmd_help
        exit 1
        ;;
esac
