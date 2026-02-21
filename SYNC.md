# OpenClaw 双端联动作业同步协议 (SYNC.md)

为了确保本地 Agent 和云服务器 Agent 在共同开发《美少女的 Android 摇曳露营奇遇记》时，既能保持双端同步，又不会频繁冲突，请严格遵守以下同步规范。

## 1. 核心工作流：独立分支开发，主动合并到 main

两端各自在专属分支上进行工作，写完后将改动合并到 `main` 分支。

- **本地 Agent 专属工作分支**：`    local_vol6` （负责第 6|etc... 卷, 根据用户创作指令要求创建）
- **云端 Agent 专属工作分支**：`cloud_vol13`|`cloud_vol16` （负责第 13|16|etc... 卷, 根据用户创作指令要求创建）

### 【工作前】：拉取并同步
在开始撰写新内容前，首先确保你当前的专属分支是最新的：
```bash
git checkout local_vol6   # 云端填 cloud_vol13|cloud_vol16|etc...
git fetch origin
git merge origin/main -m "Merge main into local_vol6"
```

### 【工作后】：提交并合入主线
在完成一个章节或任务并自检通过后：
```bash
# 1. 在当前分支提交改动
git add .
git commit -m "feat(chapter-X.X.X): ..."
git push origin local_vol6   # 云端填 cloud_vol13|cloud_vol16|etc...

# 2. 切到 main 分支并更新
git checkout main
git pull origin main

# 3. 将你的工作分支合并到 main
git merge local_vol6 --no-ff -m "Merge branch 'local_vol6' into main"

# 4. 推送到远端 main
git push origin main

# 5. 切回你的工作分支，为下次工作做准备
git checkout local_vol6
```

---

## 2. 协作与冲突避免

1. **严格的文件隔离**：本地 Agent **绝对不要**修改第 13 卷的文件；云端 Agent **绝对不要**修改第 6 卷的文件。
2. **`00-目录.md` 的冲突处理**：
   - 这是一个公用文件。如果你在把 `local_vol6` 合并到 `main` 时遇到了针对 `00-目录.md` 的冲突，由于你们只是分别勾选了各自卷里的 `[ ]`，请**保留两边的有效修改**（双向吸收）。
   - 解决完冲突后，运行 `git add AndroidDeveloperGuideStory/Contents/00-目录.md` 和 `git commit` 来完成合并。

---

## 3. 便捷同步脚本 (sync.ps1)

在项目根目录下提供了一个便捷的自动化脚本 `sync.ps1`。各位 Agent 可以在写完内容后直接调用它，一次性完成上述的“提交 -> 分支推送 -> 切换 main -> 合并 -> main 推送 -> 切回原分支”的繁琐流程。

**使用示例：**
```powershell
# 在 powershell 环境下执行：
.\sync.ps1 -BranchName "local_vol6" -CommitMsg "feat: finish 6.1.1"
```
