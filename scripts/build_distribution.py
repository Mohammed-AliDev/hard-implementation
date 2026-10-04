"""Refresh distributable file hashes and the original workflow section index."""
import hashlib
import json
from pathlib import Path
import re

from check_consistency import project_version

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_SHA256 = "3302000990ac049cc068a63927dac29757be8bd8031bb3fb9d5d7c1c715035c7"


def main():
    workflow = ROOT / "skills/hard-implementation/references/workflow.md"
    raw = workflow.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ORIGINAL_SHA256, "Original workflow changed"
    paths = sorted((p for p in (ROOT / "skills").rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"),
                   key=lambda p: p.relative_to(ROOT).as_posix())
    paths += sorted((p for p in (ROOT / "adapters").rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"),
                    key=lambda p: p.relative_to(ROOT).as_posix())
    data = {"package": "hard-implementation", "version": project_version(ROOT), "files": {
        p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (ROOT / "distribution.json").write_bytes((json.dumps(data, indent=2) + "\n").encode("utf-8"))
    original_lines = raw.decode().splitlines()
    headings = [(i, s) for i, s in enumerate(original_lines, 1)
                if re.match(r"^\d+[A-Z]?\. [A-Z]", s)
                and i > 1 and original_lines[i - 2].startswith("======")]
    assert len(headings) == 46
    lines = ["# Original workflow preservation", "",
             "The original author-supplied workflow is preserved byte-for-byte in",
             "[`workflow.md`](../skills/hard-implementation/references/workflow.md).",
             "No original rule, example, or section was deleted or shortened.", "",
             f"- SHA-256: `{ORIGINAL_SHA256}`", f"- Bytes: {len(raw)}",
             f"- Numbered sections: {len(headings)} (0–44 plus 4A)", "",
             "`SKILL.md` is a loading entrypoint. `references/execution.md` adds persistence",
             "and host adaptation; `references/systems.md` adds native-system role bindings;",
             "`references/security.md` adds the applicable Universal Security Gate.",
             "They do not replace the original workflow. Every run",
             "is instructed to read the complete original before implementation.", "",
             "| Original section | Line in preserved file |", "|---|---|"]
    lines += [f"| {title} | {number} |" for number, title in headings]
    (ROOT / "docs/PRESERVATION.md").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
