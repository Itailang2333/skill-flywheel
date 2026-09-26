# skill-flywheel 🎡

简体中文（本文件） | [English](README.en.md)

> **让 Agent 跑完活自己写技能——能力随使用复利增长。**
> Every task makes your agent stronger: a markdown-only meta-skill that makes agents sediment reusable workflows into skills, on their own.

**English TL;DR** — `skill-flywheel` is a single-folder, zero-dependency "meta-skill" for agent harnesses with a skills directory (built for DeepSeek Harness, adaptable to any host that scans `<skills-root>/<name>/SKILL.md`). Once installed, the agent reviews each finished task and, when a reusable workflow shows up, writes its own new SKILL.md — deduped, templated, and carrying its battle scars (Gotchas). The skills directory grows with every task; that compounding loop is the flywheel. Optional hard-enforcement layer (`docs/enforcement.md`) closes the "agent forgot to do it" gap.

---

## 这是什么

装上后，Agent 每次完成多步任务会自问：**这套流程可复用吗？** 可复用就当场写一本新技能书（SKILL.md）落进技能根——下次同类任务直接调书，不用从头摸索。书架随使用变厚，越转越快：

```
任务 → 自查（≥8 步？棘手坑？可复用流程？）→ 查重 → 沉淀 SKILL.md → 书架 +1 → 下次直接调用
```

**不止会写新书，还会修旧书。**每次用完一本技能，Agent 会被要求反思四问——过期？错误？缺步骤？措辞乱？发现问题当场修订再收尾。修订不限于自己写的书：升级他人/第三方技能时守三条纪律——①留痕（改动+原因+日期写进该技能本体的修订记录）②不篡身份（不冒认作者、不乱盖创作标记）③分叉记账（对上游更新防覆盖）。书架因此不光越长越大，还**越用越准**——这是飞轮的第二圈。

## 为什么不是又一堆 prompt

1. **description 触发式写法（SDO）**——description 只写触发条件与触发词、绝不摘要工作流。摘要会诱导 Agent 照摘要走捷径跳过正文（借 obra/superpowers 实证结论）。
2. **失败基线先行**——没有真实踩坑记录（Gotchas）的技能等于没验过枪。本仓库自己的 SKILL.md 里就有当着用户面被抓的编造案例当反面教材。
3. **软硬配对（可选）**——纯 SKILL.md 是软执行，Agent 会漏。`docs/enforcement.md` 给出三档可叠加的硬强制（开场注入 / 运行时刹车 / 定时兜底），把它变成"不漏"。

## 30 秒上手（DeepSeek Harness）

```bash
git clone https://github.com/b-c-maker/skill-flywheel.git
cp -r skill-flywheel ~/.dsh/skills/skill-flywheel
```

或者：把 [`install-prompt.md`](install-prompt.md) **整段**复制粘贴给 DSH——它会自己写文件（自包含，无需传文件）。

**验证**：丢给 Agent 一个 8+ 步的小任务（如"修一个 Excel 合并单元格 bug"），看它是否在同一轮末尾自动写出一本新 SKILL.md。

**其他宿主**：只要你的 Agent 框架支持"技能目录 + name/description 路由"（目录形如 `<skills-root>/<name>/SKILL.md`），把目录放进去即可；脚手架的 `--dir` 参数可指定任意技能根。

## 可选：硬强制三档

| 档 | 手段 | 管什么 |
|---|---|---|
| 一 | 会话开场注入规则文本 | 开场在场（每会话必见） |
| 二 | 运行时刹车（插件：工具调用计数 + SKILL.md 触碰检测） | 中途拉回（长任务跑飞时提醒沉淀） |
| 三 | 定时兜底（cron / 会话结束钩子，见 `watchdog-automation.md`） | 事后兜底（漏网的补沉淀） |

详见 [`docs/enforcement.md`](docs/enforcement.md)。

## 作者侧实跑数据（2026-09-26，作者私有环境，供参考而非基准测试）

- 技能书架累计 **68 本**，其中 Agent 自产 **18 本**（其余为第三方与手工安装）。
- 本机制建成**首日**即沉淀 **4 册**新技能。
- 配套红灯机制（同类补丁累积到第 3 个强制上报用户）建成**当日实弹 1 次**，拦截住一次失控的重复打补丁。
- 沉淀刹车（档二）当日实测拦截 **1 次**（长任务 11 次工具调用未沉淀，被强制拉回）。

## 出处与致谢

- 思想源自 WorkBuddy 的 skill-accumulation 机制。
- **description 学科**（触发式写法、借口-反驳表、配方优于禁令）借鉴 [obra/superpowers](https://github.com/obra/superpowers) 的 writing-skills（MIT License）——本仓库以同许可证归还社区。
- 感谢公开 Agent 技能生态（awesome-claude-code / awesome-skills 等）的启发。

## License

[MIT](LICENSE) © 2026 b-c-maker
