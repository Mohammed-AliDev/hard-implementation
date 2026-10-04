#!/usr/bin/env python3
"""Inventory native Markdown task checkboxes; never infer implementation correctness."""
import argparse
import json
import re
from pathlib import Path


def inventory(text, task_format="speckit"):
    if task_format not in ("speckit", "markdown"):
        raise ValueError("Unknown task format")
    tasks, errors, seen = [], [], set()
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            value = marker.group(1)
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        match = re.match(r"^\s*[-*+]\s+\[([ xX~])\]\s+(.*)$", line)
        if not match:
            continue
        label = match.group(2)
        task_id = re.match(r"(T\d+)\b", label) if task_format == "speckit" else re.match(r"(T\d+|WP\d+|\d+(?:\.\d+)*)(?:[.)]?\s|$)", label)
        if task_format == "speckit" and (not task_id or match.group(1) == "~"):
            errors.append(f"Line {number}: checkbox has no valid leading Spec Kit task ID (T001, etc.) or uses a non-Spec-Kit status")
            continue
        key = task_id.group(1) if task_id else f"L{number}"
        if key in seen:
            errors.append(f"Line {number}: duplicate task ID {key}")
        seen.add(key)
        tasks.append({"id": key, "checked": match.group(1).lower() == "x", "line": number,
                      "in_progress": match.group(1) == "~", "label": label})
    if not tasks:
        errors.append("No tasks found; an empty inventory is not completion")
    if fence:
        errors.append("Unclosed code fence; task inventory may be incomplete")
    return {
        "total": len(tasks),
        "checked": [t["id"] for t in tasks if t["checked"]],
        "open": [t["id"] for t in tasks if not t["checked"]],
        "tasks": tasks,
        "in_progress": [t["id"] for t in tasks if t["in_progress"]],
        "format": task_format,
        "errors": errors,
        "meaning": "Checkbox inventory only; not proof of implementation or validation",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tasks", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--format", choices=("speckit", "markdown"), default="speckit")
    args = parser.parse_args()
    try:
        result = inventory(args.tasks.read_text(encoding="utf-8"), args.format)
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f"Cannot read tasks: {exc}\n")
    print(json.dumps(result, indent=2))
    return 2 if result["errors"] else (1 if args.require_complete and result["open"] else 0)


if __name__ == "__main__":
    raise SystemExit(main())
