# skill-flywheel 🎡

[简体中文](README.md) | English (this file)

> **Every task makes your agent stronger.** A markdown-only meta-skill that makes agents sediment reusable workflows into skills — on their own.

## What is this

Once installed, the agent reviews every finished multi-step task and asks: **is this workflow reusable?** If yes, it writes a brand-new SKILL.md into the skills root by itself — deduplicated against the existing shelf, following a fixed template, and carrying its battle scars (Gotchas). Next time a similar task shows up, the agent loads that book instead of fumbling from scratch. The shelf grows with every task; that compounding loop is the flywheel:

```
task → self-check (8+ steps? tricky bug? reusable flow?) → dedup → write SKILL.md → shelf +1 → reuse next time
```

**It doesn't just write new books — it repairs old ones.** After using any skill, the agent must run the four-question reflection — outdated? wrong? missing steps? badly worded? — and fix problems on the spot before wrapping up. The loop covers skills it didn't author: upgrading third-party skills follows three disciplines — (1) leave a trail (changes + reason + date recorded in that skill's own changelog), (2) never fake authorship, (3) keep fork accounting against upstream updates. The shelf doesn't just grow — it gets **sharper with use**. That's the flywheel's second turn.

## Why it's not just another prompt pack

1. **SDO descriptions** — skill `description` fields contain only triggers and keywords, never a workflow summary. Summaries in descriptions teach the agent to shortcut around the body (empirical finding from obra/superpowers).
2. **Failure baseline first** — a skill without real Gotchas has never been fired. This repo's own SKILL.md carries a caught-red-handed fabrication case as its counter-example.
3. **Optional hard enforcement** — a bare SKILL.md is soft execution; agents do forget. `docs/enforcement.md` offers three stackable layers (session-start injection / runtime brake / watchdog automation) that close the gap.

## 30-second start (DeepSeek Harness)

```bash
git clone https://github.com/b-c-maker/skill-flywheel.git
cp -r skill-flywheel ~/.dsh/skills/skill-flywheel
```

Or paste [`install-prompt.md`](install-prompt.md) **whole** into DSH — it writes the files itself (self-contained, no file transfer needed).

**Verify**: give the agent an 8+ step task (e.g. "fix a merged-cells bug in this Excel"), and check whether it writes a new SKILL.md at the end of that same turn.

**Other hosts**: anything that routes skills via a directory scan (`<skills-root>/<name>/SKILL.md`) works — drop the folder in; the scaffold's `--dir` flag targets any root.

## Optional: three layers of hard enforcement

| Layer | Mechanism | What it covers |
|---|---|---|
| 1 | Session-start injection of a rules file | Presence at开场 — every session sees the rules |
| 2 | Runtime brake (plugin: tool-call counter + SKILL.md-touch detection) | Mid-task pullback when the agent drifts |
| 3 | Watchdog automation (cron / session-end hook, see `watchdog-automation.md`) | After-the-fact sweep for missed sedimentation |

Details in [`docs/enforcement.md`](docs/enforcement.md).

## Real-world numbers from the author's setup (2026-09-26, private environment — reference, not a benchmark)

- Skills shelf: **68 books** total, **18** agent-authored (the rest third-party or manually installed).
- **4 new skills** sedimented on day one of the mechanism.
- The red-light rule (3rd same-type patch must be escalated to the user) fired **once on its first day live**, catching a runaway patch loop.
- The runtime brake fired **once** on day one (11 tool calls without sedimentation → pulled back, sedimented properly).

## Origin & acknowledgments

- The idea originates from the **skill-accumulation** mechanism of WorkBuddy.
- The description discipline (SDO, excuse-refutation tables, recipes-over-prohibitions) draws on [obra/superpowers](https://github.com/obra/superpowers) writing-skills (MIT License) — this repo gives back under the same license.
- Thanks to the open agent-skills ecosystem (awesome-claude-code / awesome-skills and friends) for the inspiration.

## License

[MIT](LICENSE) © 2026 b-c-maker
