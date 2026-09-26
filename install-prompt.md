# 安装提示词：复制粘贴给 DeepSeek Harness

把下面**整段**发给 DSH（直接粘贴到对话框），DSH 会自动创建 skill-flywheel 技能目录与文件。内容已内联，**无需事先传文件、不依赖源目录**，在任意装了 DSH 的机器上都可直接写。

> 本文件是磁盘 `SKILL.md` 与 `scripts/new_skill.py` 的**逐字克隆**，与源文件零偏差。

---

请你（DeepSeek Harness）执行以下安装：把两个文件写到你的技能搜索路径下。

目标根目录：`~/.dsh/skills/skill-flywheel/`
（若你的 skills 实际根目录不同，请改为你的技能根；写完后回显目录树确认。）

===FILE: SKILL.md===
---
name: skill-flywheel
description: 让任何加载它的 Agent 在任务结束后主动把可复用工作流固化成 skill——元技能，教 Agent 生产更多技能。触发条件：完成 8+ 工具调用的多步任务后；修好棘手报错/挖出非显然 workaround 后；发现可复用流程；用户要求把流程写成 skill。触发词：沉淀、写成 skill、固化流程、技能自沉淀。
agent_created: true
---

# Skill Flywheel（技能自沉淀）

把平台强制层的「技能自沉淀 + 反思纠错」机制通用化成一个可安装的 skill，使任何加载了它的 Agent——包括通过承载器或独立技能目录运行的 **DeepSeek Harness (DSH)**——都能在任务结束后**主动把可复用的工作流固化成 skill**，而不是只留存在对话历史里。

> **本质**：本 skill 是"元 skill"——它教 Agent 如何生产更多 skill。装上它，Agent 跑完活会自己写 SKILL.md，复利滚动。思想出处见根目录 README「出处与致谢」。

## When to use

- 刚跑完一个多步任务（8+ 工具调用）后，需要决定要不要沉淀。
- 修好一个 tricky 报错 / 挖出一个非显然的 workaround 后。
- 发现一条明显可复用的流程（脚本组合、文件操作套路、跨工具协作顺序）。
- 用户要求"把这套机制/流程写成 skill 装上"。

## 心智模型（先读这段）

- **Skill = 可执行 playbook；Memory = 信息备忘录。** 能复用的"怎么做"走 Skill；跨项目的人设/偏好走 Memory（你平台的记忆工具或记忆文件）。
- 装了平台强制层的，规则是**强制**的：完成多步任务后必须沉淀，除非是一锤子买卖 / 含未脱敏敏感信息 / 已有同名 skill 完整覆盖。
- 沉淀要在**同一轮**完成——写完交付物 → 立刻写 skill（平台有 SkillManage 类工具就用它；DSH 侧没有，直接用文件工具写 `~/.dsh/skills/<name>/SKILL.md`）→ 再回复用户。**不要等用户催**。
- 仅自己创建的 skill（`agent_created: true`）才用 `SkillManage(modify)` 回写；DSH 侧无此硬锁，但升级他人技能守纪律（见 Gotchas）。
- **DSH 落盘收尾**：沉淀完成后，若你的环境配置了技能名册/索引生成器则运行之刷新快照（无则跳过），并在最终回复报告新技能的安装位置与触发方式。
- **落笔前查重（DSH）**：新建前先读技能名册/索引（如有）或 grep 技能根目录既有技能的 name、description、触发词；同一摊活已有手册 → 把新内容并入该 SKILL.md（改完刷新名册），**禁止新建同岗位第二本**；代装候选同样先查重。DSH 扫描器只查重名字不查重内容，书名不同照单全收——这道关只能自己把。
- **沙箱感知（自动化/受限会话）——回退两岔**：工作区专用技能 → 直接写项目级技能根 `<工作区>/.agents/skills/<名>/SKILL.md`（工作区内沙箱通常允许、立即可用）；跨工作区/用户级技能 → 用户级直写最多 1 次，被拒即改写 `<工作区>/.workbuddy/技能候选/<名>/SKILL.md`（frontmatter 必须正规——引用块式元数据扫描器不认）并在收尾回复上报「技能候选待装：<名>｜<一句话描述>」；禁止删候选副本、禁止假报成功（成败只看 stderr 与实物）。两扇门落笔前都要查重。若配置了硬强制层，主会话开场会收到「候选技能待装」提醒（带已装去重），收到提醒或用户要求时按代装流程处理（校验 → 装 → 刷新名册 → 清候选），受限会话跳过此步。

## 触发规则（mandatory，满足任一即触发）

1. 工具调用 **≥ 8** 且任务含 **≥ 3** 个可独立验证的步骤。
2. 修好一个 **tricky error**（环境坑、版本不兼容、跨文件陷阱、权限被拒）。
3. 发现**非显然可复用 workflow**（如"先确认源文件路径再渲染对应页"这种反跨文件陷阱；或"整表重建比 delete_rows 更安全"这种 Excel 套路）。

**跳过（不沉淀）**：
- 任务明显一次性、无复用价值。
- 含敏感信息（密钥 / 权限结论未脱敏）——宁可写 Memory 也不写 skill。
- 已有同名 skill 完整覆盖该流程。

## SKILL.md 模板（落盘格式）

```markdown
---
name: <kebab-case-唯一名>
description: <只写触发条件与触发词（何时用/症状），禁止写工作流摘要；宿主靠这字段路由>
agent_created: true
---

# <人类可读标题>

<一两句定位：这是什么 skill，解决什么痛点>

## When to use
- <触发场景 1>
- <触发场景 2>

## 心智模型（先读这段）
- <核心类比 / 必须前置理解的约束>

## 怎么做（playbook）
1. <步骤，含可直接抄的脚本/命令>
2. <步骤>
3. <收尾：更新索引/变更日志/回执>

## 关键脚本
<内嵌或指向 scripts/ 下的可复用脚本；脚本必须自包含、零外部依赖优先>

## Gotchas / 踩坑（从实战学到）
- <失败模式 + 根因 + 修复；这是 skill 最有价值的部分>

## 存储与复用
- 所在技能根路径 + 触发方式
```

## 沉淀三铁律（借 obra/superpowers writing-skills，MIT）

1. **description 触发式写法（SDO）**：只写「Use when…/触发词/症状」，**绝不摘要工作流**——description 含流程摘要时 Agent 会照摘要走捷径、跳过正文。技能名只用字母/数字/连字符——**下划线开头会被 DSH 加载器拒识（invalid skill name，实测）**。
2. **失败基线先行**：沉淀前若存在真实失败案例（报错/事故/死循环/返工），必须把「当时怎么失败的+根因+修法」写进 Gotchas；没有失败基线的技能等于没验过枪。
3. **借口-反驳表 + 配方优于禁令**：纪律型技能（强制流程类）加「常见借口→反驳」表与红旗清单；规则文本优先写「输出应长什么样」（配方），少用「别做什么」——禁令对塑造型问题实测更有害。

## 反思 / 纠错闭环（mandatory）

- 加载并使用过某 skill 后，必须反思：过期？错误？缺步骤？措辞乱？
  - 内心自问即可，不需要每次打断用户。
- 有改进 → 立即修订该 skill（平台有 SkillManage 用之；否则编辑文件），再回复。典型改进：修 typo/错工具名；补遗漏步骤；加一条实测踩坑（Gotchas 段）。
- 没改进 → **不要为了 churn 去改**。
- 若发现已有 skills 明显重复/冲突/过期，在最终回复里提醒用户整理（不要擅自批量删）。

## 脚手架脚本

`scripts/new_skill.py`：从 `--name` / `--description` / `--body`(或 `--body-file`) 一键生成带 frontmatter 的 `SKILL.md`，自动建目录。用法：

```bash
python <skill基目录>/scripts/new_skill.py \
    --name "my-new-skill" \
    --description "一句话定位" \
    --body-file "/tmp/body.md"
# 或正文直接传：--body "$(cat <<'MD' ... MD)"
# skill 基目录：DSH=~/.dsh/skills/skill-flywheel/
```

## 存储位置

| 环境 | 路径 |
|------|------|
| DSH（用户级） | `~/.dsh/skills/<name>/SKILL.md` |
| DSH（项目级） | `<工作区>/.agents/skills/<name>/` |
| 其他宿主 | 该宿主的技能搜索路径/技能根，整目录放入即生效 |
| 随承载器 | `<承载器>/skills/<name>/`，随初始化一步铺设到客户机 |

## 触发机制真相（务必先读，避免误判"自动"）

本 skill 是**纯指令型 SKILL.md**，不是后台 daemon / 钩子 / 定时任务。它**不安装任何事件订阅或自动进程**。

- **"自动"的真正来源**：SKILL.md 被加载进 Agent 上下文后，Agent 的推理循环在每轮收尾**主动选择遵守**规则（≥8 步就写 skill）。这是 **LLM 软执行**，靠指令在上下文里"提醒"，**不是平台硬强制**。
- **与平台强制层的差异**：作者内部生产平台把该机制写进**系统提示强制段**，平台层保证执行；DSH 默认无此层，本 skill 是 DSH 侧唯一执行保障，弱一档——Agent 可能漏（skill 不在上下文 / 被长任务挤掉注意力时）。
- **想更硬（可选增量）**：见 `docs/enforcement.md`——会话开场注入 / 运行时刹车 / 定时兜底三档，可叠加。本 skill 基线**不含**这些，需另配。
- **生成的 skill 单独起名**：每次沉淀产出**独立的新 SKILL.md**（kebab-case 名由 Agent 按主题取，如 `excel-merge-rebuild`），不覆盖本 skill。
- **也支持手动触发**：用户直接调用本 skill（或自然语言"把这套流程写成 skill"）可让 Agent **立即**沉淀当前/指定对话，不必等自动判定。

## DSH 安装说明

**关键区分：markdown SKILL.md vs code plugin**

本 skill 面向**纯 markdown playbook**，生成的也是 SKILL.md。这类在 DSH 里：

- **"安装" = 放进技能搜索路径**。DSH 靠**扫描目录 + name/description 路由**发现它，不需要 plugin 的 dependencies/bundles 注册，也不需要 build。放进去，下一轮就被路由到。
- 如果沉淀的是**带代码的 plugin（TS/JS）**，那才走普通 plugin 注册。本 skill 模板默认产出 markdown，走"放目录即生效"这条路。

步骤：
1. 取本仓库 `skill-flywheel/` 目录（含 `SKILL.md` + `scripts/new_skill.py`）。
2. 整目录复制到 DSH 技能根：独立装 `~/.dsh/skills/skill-flywheel/`；随承载器装 `<承载器>/skills/skill-flywheel/`。
3. DSH 按 name+description 做意图路由；装上后 Agent 跑完多步任务会**主动触发本 skill** 去生产更多 skill（软执行，见上）。
4. 验证：让 DSH 跑一个 8+ 步的小任务（如"修一个 Excel 合并单元格 bug"），看它是否在同一轮末尾写出新 `SKILL.md`。
5. **新生成的 skill 同样落盘到技能目录即"注册"**。

> ⚠️ DSH 默认**没有**技能自沉淀机制——它只是 "Everything-is-a-Plugin" 框架，不会自发沉淀。本 skill 就是补上这一层（软执行）。装好后，Agent 能力随使用复利增长；若需硬保障，另配三档硬强制（见 docs/enforcement.md）。

## 同包附带的安装/加固提示词

- `install-prompt.md`：**自包含安装提示词**，复制粘贴给 DSH 即可直接写文件（SKILL.md + new_skill.py 已内联），不依赖源目录，任意机器可用。
- `watchdog-automation.md`：**cron / 会话结束钩子注册提示词**，把本技能的"软执行"升级为"有守护进程兜底"，接近平台强制层的"不漏"水平。

## Gotchas（从实战学到，避免重蹈）

- **跨文件陷阱（最高频）**：用户指明页码/幻灯片/行号时，**先确认源文件路径（pdf/pptx/xls）→ 再取该文件对应位置的实际内容 → 最后下结论**。严禁因"页码相同"就跨文件假设内容一致。
- **Excel (1) 副本覆盖主文件视图**：Excel 开着某文件时可能生成 `文件名 (1).xlsx` 恢复副本 + `~$文件名.xlsx` 锁文件；**用户看到的活视图可能是 (1) 副本**。写前先查副本与锁文件；怀疑"写入没生效"先 dump 两份比对。
- **整表重建比 delete_rows 安全**：section 行数变化时，清空目标区域 + 按运行行号重填 + 重挂 merge/样式，比 `delete_rows`（不更新 merged ranges，易留僵尸合并）更稳。
- **SkillManage 权限边界**：平台工具只能改 `agent_created: true` 的 skill；系统自带 skill 不要擅改。升级他人/第三方技能守三条纪律：①留痕（改动+原因+日期写入技能本体的修订记录）②不篡身份（不盖 agent_created 章、不改名）③第三方分叉记账（防上游更新覆盖）。
- **宣传模式 = 编造高发区**：写 README/汇报等"卖货文案"时，战果数字与资历叙事**同样适用实物指针纪律**——实测案例：起草开源 README 时把"机制首日实跑"夸成"实跑数月"、把整架书（多数为第三方）归功于本机制，被用户当场抓获。修法：文案里每个战果必须能指到台账/名册/命令实物，指不到就删；真话本身够用，不需要吹。
- **敏感信息绝不进 skill**：密钥、未脱敏权限结论、客户真实 open_id 写 Memory 或加密配置，不写 skill 正文。

## 参考（本 skill 的设计来源）

- 思想源自 WorkBuddy 的 skill-accumulation 机制（详见 README「出处与致谢」）。
- obra/superpowers writing-skills（MIT）：description 触发式写法（SDO）、借口-反驳表、配方优于禁令。

## 修订记录

- 2026-09-26 v0.1.0：自内部版本通用化开源——去除私有路径与业务实证，技能名定为 skill-flywheel；Gotchas 增补"宣传模式 = 编造高发区"（开源前自查实测发现）。
===END===

===FILE: scripts/new_skill.py===
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new_skill.py — Skill Flywheel 脚手架

从 --name / --description / --body(或 --body-file) 一键生成带 frontmatter 的 SKILL.md，
自动建目录。零外部依赖（仅标准库）。

用法:
  python new_skill.py --name "my-skill" --description "一句话定位" --body-file /tmp/body.md
  python new_skill.py --name "my-skill" --description "一句话定位" --body "# 标题\n内容..."
"""
import argparse
import os
import sys


def main():
    ap = argparse.ArgumentParser(description="Scaffold an agent SKILL.md")
    ap.add_argument("--name", required=True, help="kebab-case 唯一名（只用字母/数字/连字符）")
    ap.add_argument("--description", required=True, help="一句话定位（只写触发条件与触发词），用于意图路由")
    ap.add_argument("--dir", default=None,
                    help="skill 根目录，默认 ~/.dsh/skills（可用此参数覆盖为你的宿主技能根）")
    ap.add_argument("--body", default=None, help="markdown 正文（或改用 --body-file）")
    ap.add_argument("--body-file", default=None, help="读取 markdown 正文文件")
    args = ap.parse_args()

    root = args.dir or os.path.join(os.path.expanduser("~"), ".dsh", "skills")
    skill_dir = os.path.join(root, args.name)
    os.makedirs(skill_dir, exist_ok=True)

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            body = f.read()
    else:
        body = args.body or ""

    # 去掉正文首尾空白，避免多余空行
    body = body.strip() + "\n"

    front = (
        "---\n"
        f"name: {args.name}\n"
        f"description: {args.description}\n"
        "agent_created: true\n"
        "---\n\n"
    )

    out = os.path.join(skill_dir, "SKILL.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(front + body)

    print(f"[OK] wrote {out}")
    print(f"[OK] skill dir: {skill_dir}")


if __name__ == "__main__":
    main()
===END===

安装后请：
1. 列出 `~/.dsh/skills/skill-flywheel/` 确认 `SKILL.md` 与 `scripts/new_skill.py` 都在；
2. 说明本技能是"软执行"元技能（见 SKILL.md 的「触发机制真相」），仅靠指令在上下文提醒 Agent 自动沉淀；
3. 如需硬保障，建议再按 `docs/enforcement.md` 配置硬强制，或注册一个 cron/会话结束自动化（见同包 `watchdog-automation.md`）。
