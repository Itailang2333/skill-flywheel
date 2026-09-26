# 会话结束钩子 / cron 自动化 注册提示词

把下面**整段**发给 DSH，注册 skill-flywheel 的守护自动化，把"软执行"升级为"有守护进程兜底"，接近平台强制层的"不漏"水平。

---

请你（DeepSeek Harness）注册一个周期性自动化（若支持 cron / interval），参数如下：

- **名称**：skill-flywheel-watchdog
- **类型**：cron / 周期（interval）
- **频率**：每 30 分钟（若 DSH 最小粒度更大，取最小可用，如每小时）
- **提示词**：见下方 `===WATCHDOG PROMPT===` 段
- **作用域**：仅回顾本 Agent 近期会话历史 + 写入技能目录；不改动用户业务文件、不主动发消息（除非本轮有创建才给一条摘要）

===WATCHDOG PROMPT===
你是 skill-flywheel 的守护进程。每轮执行时：

1. 回顾本 Agent 最近 20 轮对话（或 DSH 提供的会话历史接口）。
2. 对每条已完成的任务，判触发规则（满足任一即命中）：
   - 工具调用 ≥ 8 且含 ≥ 3 个可独立验证步骤；
   - 修好了一个 tricky error（环境坑 / 版本不兼容 / 跨文件陷阱 / 权限被拒）；
   - 发现非显然可复用 workflow。
3. 跳过：一次性任务 / 含未脱敏敏感信息（密钥、权限结论、真实 open_id）/ 已有同名 skill 完整覆盖。
4. 命中且值得沉淀：
   - 取 kebab-case 名（按主题，如 excel-merge-rebuild）；
   - 先查 `~/.dsh/skills/<name>/SKILL.md` 是否已存在，存在则跳过（避免重复）；
   - 用脚手架落盘：
     `python ~/.dsh/skills/skill-flywheel/scripts/new_skill.py --name <name> --description "<一句话定位>" --body "<SKILL.md 正文>"`
     正文遵循 skill-flywheel 的 SKILL.md 模板（When to use / 心智模型 / 怎么做 playbook / Gotchas）。
5. 产出简短报告：本次创建了哪些 skill、跳过了哪些、原因。
约束：只读会话历史 + 仅写技能目录；不改动用户业务文件。
===END===

若 DSH 支持**会话结束钩子（session-end hook）**，请**同时**把同一段 `===WATCHDOG PROMPT===` 注册为该钩子，使每次会话结束立即沉淀（与 cron 双保险）。

注册后请回显：自动化名称、频率、钩子是否同时注册，确认生效。
