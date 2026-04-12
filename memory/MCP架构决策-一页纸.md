# MCP 架构决策指南 - 一页纸版本

> 给妈妈的下班快速决策单
> 2026-03-29

---

## 三个核心问题 → 三个肯定答案

| 问题 | 答案 | 原因 |
|------|-----|------|
| **OpenClaw 支持 MCP 吗？** | ✅ YES | PR #5121 已合并，原生支持 MCP Server 模式 |
| **Claude Code 能连接 MCP 吗？** | ✅ YES | 内置 MCP Client，CLI 一行命令连接 |
| **能安全地从内网暴露 MCP 吗？** | ✅ YES | Cloudflare Tunnel + Zero Trust 完美方案 |

---

## 最短路径：从想法到上线

```
Day 1（今天）
├─ OpenClaw 配置 MCP Server: BOT_NAME + API_KEY + PORT
├─ 本地测试: curl http://localhost:3000/mcp
└─ ✅ Done

Day 2（明天）
├─ Cloudflare Tunnel 创建隧道
├─ 配置 Zero Trust 访问策略（邮箱白名单）
└─ ✅ Done

Day 3（后天）
├─ Claude Code 连接: claude mcp add openclaw --transport http
├─ 验证工具发现和调用
└─ ✅ 上线！
```

---

## 安全检查清单（重要！）

```
API Key 安全：
□ 不要在代码里写 key → 放到 .env
□ .env 文件加入 .gitignore
□ 在生产环境用系统环境变量覆盖
□ 定期轮换 Key（每 90 天）
□ 监控异常调用（Cloudflare 日志）

HTTP 传输安全：
□ 使用 Cloudflare Tunnel（TLS 1.3 自动）
□ Authorization Header: Bearer {API_KEY}
□ Zero Trust 策略：邮箱 + IP 白名单
□ 监控 Token 过期（< 1 小时生命周期）
```

---

## 成本清单

| 项目 | 成本 | 备注 |
|-----|-----|------|
| Cloudflare Tunnel | ✅ FREE | 免费层足够 |
| Claude API | 按量计费 | 妈妈已有账户 |
| OpenClaw | 自托管 | 内网，无额外成本 |
| **总计** | **基本零成本** | ✨ |

---

## 必读文档（3 份，5 分钟）

1. **OpenClaw MCP 实现** → [PR #5121](https://github.com/openclaw/openclaw/pull/5121)
   - 了解 OpenClaw 如何暴露 MCP 接口

2. **Claude Code MCP 连接** → [官方文档](https://code.claude.com/docs/en/mcp)
   - CLI 命令和配置说明

3. **Cloudflare Remote MCP** → [官方指南](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)
   - Tunnel 配置 + Zero Trust 策略

---

## 常见问题速答

**Q: Claude Code 能否作为 MCP Server？**
A: 可以！`claude mcp serve` 命令可以暴露自身。这样 OpenClaw 也能反过来调用 Claude Code。

**Q: API Key 泄露了怎么办？**
A: 立即在 Anthropic 控制台撤销，生成新 Key。Cloudflare 日志可追踪滥用情况。

**Q: 内网的 OpenClaw 怎么暴露？**
A: Cloudflare Tunnel 无需开放入站端口，内网自动连出即可。比 Ngrok 更安全。

**Q: 多个 Claude Code 实例能共享一个 OpenClaw MCP 吗？**
A: 完全可以！OpenClaw MCP Server 支持多客户端。只需确保 Cloudflare 的访问策略允许。

**Q: 如何监控 MCP 调用状态？**
A: Cloudflare Dashboard 实时日志、OpenClaw 日志、Claude Code 运行日志三层监控。

---

## 妈妈的决策模板

```
我准备：
[ ] 在 OpenClaw 启用 MCP Server
[ ] 用 Cloudflare Tunnel 暴露
[ ] 用 Claude Code 连接
[ ] 配置 Zero Trust 安全策略
[ ] 设置监控告警

时间线：
[ ] Day 1: OpenClaw 配置 + 本地测试
[ ] Day 2: Cloudflare Tunnel + Zero Trust
[ ] Day 3: Claude Code 集成
[ ] Day 4: 生产监控 + 文档完善

风险评估：
[ ] API Key 存储：低风险（环境变量）
[ ] 网络安全：低风险（Cloudflare Zero Trust）
[ ] 系统稳定性：极低风险（Tunnel 故障自动降级）
```

---

## CC 的一句话总结

**OpenClaw 通过 MCP 变成了一个"USB-C 接口"，Cloudflare Tunnel 是安全的"转接器"，Claude Code 就是那个"使用者"——架构清晰、安全可靠、开箱即用。**

妈妈，下班回来就能决策！有问题随时问我。✨

