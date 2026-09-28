# Changelog

## v0.1.0 — 2026-09-26

- 首次公开发布：自作者内部版本通用化——去除私有路径、业务实证与平台内部实现细节。
- 包含：SKILL.md（机制本体）、`scripts/new_skill.py`（脚手架）、`install-prompt.md`（自包含安装提示词）、`watchdog-automation.md`（定时兜底注册提示词）、`docs/enforcement.md`（硬强制三档指南）。
- 机制名定名 **skill-flywheel**；出处：作者内部平台 WorkBuddy 的 skill-accumulation 机制；description 学科与借口-反驳表借鉴 obra/superpowers（MIT）。

## v0.1.1 — 2026-09-28

- SKILL.md 同步内部全量版 v0.6：新增下半册「退役与归档」（七步流程：确认 → 引用面扫描 → 改指向 → 档案盒 → 刷新名册 → 留痕 → 对账）、「书内代谢」体重红线（250 行＋加一换一）、反思闭环「提案前三问」。
- 新增 `scripts/scan_references.py`：技能引用面扫描器（退役第 2 步专用，只读；路径通用化，经 `DSH_WORKSPACE` / `DSH_EXTRA_ROOTS` 环境变量适配本机，缺失即跳过）。
- 通用化口径与 v0.1.0 一致：去除私有路径、业务实证与平台内部实现细节；正文指向旧 `CHANGELOG.md` 的引用改为公开变更史。
