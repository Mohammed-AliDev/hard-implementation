#!/usr/bin/env python3
"""Read-only discovery of native spec artifacts; never select an ambiguous target."""
import argparse
import json
from pathlib import Path
import re


def discover(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"Repository directory does not exist: {root}")
    candidates = []

    def files(paths):
        result = []
        for p in paths:
            p = Path(p).resolve()
            if p.is_file() and p.resolve().is_relative_to(root) and not any(part in ("archive", "archived") for part in p.relative_to(root).parts):
                result.append(p.relative_to(root).as_posix())
        return sorted(set(result))

    def add(system, target, requirements, design, queue, metadata=()):
        roles = {"requirements": files(requirements), "design": files(design), "queue": files(queue)}
        if not any(roles.values()):
            return
        missing = [role for role in ("requirements", "queue") if not roles[role]]
        if system not in ("OpenSpec", "Superpowers") and not roles["design"]:
            missing.append("design")
        candidates.append({"system": system, "target": target.relative_to(root).as_posix(),
                           **roles, "metadata": files(metadata), "missing": missing,
                           "ready": not missing,
                           "meaning": "Artifact availability only; approvals and task evidence still require inspection"})

    for target in sorted((root / "specs").glob("*")):
        if target.is_dir():
            add("Spec Kit", target, [target / "spec.md"], [target / "plan.md"], [target / "tasks.md"])
    for target in sorted((root / ".kiro/specs").glob("*")):
        if target.is_dir():
            # cc-sdd installs Kiro-compatible specs; spec.json provides phase/approval metadata.
            system = "cc-sdd" if (target / "spec.json").is_file() else "Kiro Specs"
            add(system, target, [target / "requirements.md"], [target / "design.md"], [target / "tasks.md"], [target / "spec.json"])
    for target in sorted((root / ".spec-workflow/specs").glob("*")):
        if target.is_dir():
            add("Spec Workflow MCP", target, [target / "requirements.md"], [target / "design.md"], [target / "tasks.md"])
    for target in sorted((root / "openspec/changes").glob("*")):
        if target.is_dir() and target.name not in ("archive", "archived"):
            add("OpenSpec", target, (target / "specs").glob("*/spec.md"), [target / "design.md"],
                [target / "tasks.md"], [target / "proposal.md", target / ".openspec.yaml", root / "openspec/config.yaml"])
    for target in sorted((root / "kitty-specs").glob("*")):
        if target.is_dir():
            packages = list((target / "tasks").glob("WP*.md")) + list((target / "tasks").glob("*/WP*.md"))
            add("Spec Kitty", target, [target / "spec.md"], [target / "plan.md"],
                packages or [target / "tasks.md"], [target / "meta.json"])
    for target in sorted((root / "conductor/tracks").glob("*")):
        if target.is_dir():
            add("Conductor", target, [target / "spec.md"], [target / "plan.md"], [target / "plan.md"],
                [target / "metadata.json", root / "conductor/tracks.md", root / "conductor/workflow.md"])
    for folder in (root / "docs/superpowers/plans", root / "docs/plans"):
        for plan in sorted(folder.glob("*.md")):
            if not plan.resolve().is_relative_to(root):
                continue
            text = plan.read_text(encoding="utf-8")
            if "Implementation Plan" not in text and not re.search(r"^### Task \d+", text, re.M):
                continue
            match = re.search(r"^\*\*Spec:\*\*\s*[`\[]?([^\n`\]]+)", text, re.M)
            req = []
            if match:
                reference = match.group(1).strip()
                linked = re.search(r"\[[^]]+\]\(([^)]+)\)", text[match.start():].splitlines()[0])
                if linked:
                    reference = linked.group(1)
                path = root / reference
                if not path.is_file():
                    path = plan.parent / reference
                req = [path]
            add("Superpowers", plan, req, [plan], [plan])
    candidates.sort(key=lambda item: (item["system"], item["target"]))
    selection = ("One candidate found; inspect its native gates before implementation." if len(candidates) == 1
                 else "Multiple candidates: use explicit target/context; do not choose by modification time." if candidates
                 else "No standard-layout candidates found. Inspect repository instructions and custom artifact locations; do not create a Spec Kit scaffold.")
    return {"repository": str(root), "candidates": candidates, "selection": selection,
            "selected": candidates[0]["target"] if len(candidates) == 1 else None,
            "limitations": "Conventional-layout discovery only; custom schemas, branches, and native approval/board states need agent inspection."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        print(json.dumps(discover(args.repository), indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Cannot discover specification artifacts: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
