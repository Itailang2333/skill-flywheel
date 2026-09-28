# -*- coding: utf-8 -*-
"""scan_references.py — 技能引用面扫描器（skill-flywheel 下半册第 2 步专用，只读）

在技能书架全部 .md/.py、名册（skills-data.json）、自动化总账本、各工作区补丁台账（若存在）
里 grep 指定技能名。输出 文件:行号:内容；本尊目录命中标「本尊」。退出码恒 0（只读核对工具）。

本机适配（全部可选，缺失即跳过）：
- DSH_WORKSPACE   主工作区根目录（其下的 skills-data.json 与 补丁台账.md 入扫）
- DSH_EXTRA_ROOTS 追加根目录列表（os.pathsep 分隔），各根下的 补丁台账.md 入扫
"""
import argparse
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = os.path.expanduser("~")


def iter_targets():
    skills = os.path.join(HOME, ".dsh", "skills")
    for root, dirs, files in os.walk(skills):
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]
        for f in files:
            if f.endswith((".md", ".py")):
                yield os.path.join(root, f)
    ws = os.environ.get("DSH_WORKSPACE", "")
    if ws:
        yield os.path.join(ws, "skills-data.json")
        yield os.path.join(ws, "补丁台账.md")
    extra = os.environ.get("DSH_EXTRA_ROOTS", "")
    for root in [x for x in extra.split(os.pathsep) if x]:
        yield os.path.join(root, "补丁台账.md")
    yield os.path.join(HOME, ".dsh", "storages", "dsh_automation.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="要扫的技能名（目录名）")
    a = ap.parse_args()
    needle = a.name
    self_marker = os.path.join(HOME, ".dsh", "skills", needle) + os.sep
    hits = 0
    for path in iter_targets():
        if not os.path.isfile(path):
            continue
        try:
            with io.open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if needle in line:
                        hits += 1
                        tag = "本尊" if path.startswith(self_marker) else "外部"
                        print("[%s] %s:%d:%s" % (tag, path, i, line.strip()[:200]))
        except OSError as e:
            print("[跳过] %s (%s)" % (path, e))
    print("== 「%s」共 %d 处命中（本尊=该技能自己目录内，属正常；外部命中须逐处改指向后才准入档案盒） ==" % (needle, hits))
    sys.exit(0)


if __name__ == "__main__":
    main()
