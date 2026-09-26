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
