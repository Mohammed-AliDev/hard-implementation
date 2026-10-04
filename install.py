# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Install the complete skill into a project for Codex and/or OpenCode."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tempfile
from urllib.request import urlopen

REPOSITORY = "Mohammed-AliDev/hard-implementation"
RELEASE = "v1.0.1"
STATE = ".hard-implementation/install.json"
SKILL_PREFIX = "skills/hard-implementation/"
DEST_PREFIX = ".agents/skills/hard-implementation/"
ADAPTER = "adapters/opencode/hard.implement.md"
COMMAND = ".opencode/commands/hard.implement.md"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def valid_relative(name):
    return (isinstance(name, str) and bool(name) and "\\" not in name
            and ":" not in name and not name.startswith("/")
            and all(p not in ("", ".", "..") for p in name.split("/")))


def managed_name(name):
    return valid_relative(name) and (name.startswith(DEST_PREFIX) or name == COMMAND)


def safe_path(root, name):
    if not valid_relative(name):
        raise ValueError(f"Invalid relative path: {name!r}")
    current = root
    parts = PurePosixPath(name).parts
    for index, part in enumerate(parts):
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Refusing symlink destination: {current}")
        if index < len(parts) - 1 and current.exists() and not current.is_dir():
            raise ValueError(f"Destination parent is not a directory: {current}")
    return current


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".hard-implementation-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def load_state(root):
    path = safe_path(root, STATE)
    if not path.exists():
        return {"files": {}, "agents": []}
    state = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(state, dict) or state.get("package") != "hard-implementation":
        raise ValueError("Unrecognized installation record")
    if not isinstance(state.get("files"), dict) or not isinstance(state.get("agents"), list):
        raise ValueError("Invalid installation record")
    if any(a not in ("codex", "opencode") for a in state["agents"]):
        raise ValueError("Invalid agent in installation record")
    for name, sha in state["files"].items():
        if not managed_name(name) or not isinstance(sha, str) or len(sha) != 64:
            raise ValueError("Invalid managed file in installation record")
    return state


def read_source(source, name):
    if not valid_relative(name):
        raise ValueError("Invalid package source path")
    if source:
        return safe_path(source, name).read_bytes()
    url = f"https://raw.githubusercontent.com/{REPOSITORY}/{RELEASE}/{name}"
    with urlopen(url, timeout=30) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError(f"Package file is too large: {name}")
    return data


def payload(source, agents):
    manifest = json.loads(read_source(source, "distribution.json"))
    if manifest.get("package") != "hard-implementation" or manifest.get("version") != RELEASE[1:]:
        raise ValueError("Wrong package or release in distribution manifest")
    files = manifest.get("files")
    if not isinstance(files, dict) or SKILL_PREFIX + "SKILL.md" not in files:
        raise ValueError("Incomplete distribution manifest")
    required = ["references/workflow.md", "references/execution.md",
                "assets/implementation-state.md", "scripts/audit_tasks.py"]
    if any(SKILL_PREFIX + name not in files for name in required) or ADAPTER not in files:
        raise ValueError("Required workflow resources or adapter missing")
    result = {}
    for name, sha in files.items():
        if not valid_relative(name):
            raise ValueError("Invalid source path in distribution manifest")
        if name.startswith(SKILL_PREFIX):
            destination = DEST_PREFIX + name[len(SKILL_PREFIX):]
        elif name == ADAPTER:
            if "opencode" not in agents:
                continue
            destination = COMMAND
        else:
            raise ValueError(f"Unexpected package resource: {name}")
        data = read_source(source, name)
        if digest(data) != sha:
            raise ValueError(f"Checksum mismatch: {name}")
        result[destination] = data
    return result


def install(root, source, agents, dry_run=False, uninstall=False):
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")
    old = load_state(root)
    chosen = sorted(set(agents) | set(old["agents"]))
    desired = {} if uninstall else payload(source, chosen)
    owned = {}
    writes, removals = {}, []
    # Preflight the entire operation before modifying any destination.
    for name in sorted(set(old["files"]) | set(desired)):
        path = safe_path(root, name)
        present = path.exists()
        if present and not path.is_file():
            raise ValueError(f"Destination is not a file: {path}")
        current = path.read_bytes() if present else None
        if name in old["files"]:
            if current is not None and digest(current) != old["files"][name]:
                raise ValueError(f"Locally modified managed file; preserve or move it first: {path}")
        elif current is not None:
            if current != desired[name]:
                raise ValueError(f"Existing unowned file; refusing to overwrite: {path}")
            # An identical pre-existing file is usable but is never claimed/deleted.
            continue
        if name in desired:
            owned[name] = digest(desired[name])
            if current != desired[name]:
                writes[name] = desired[name]
        elif present:
            removals.append(name)
    actions = {"write": sorted(writes), "remove": removals, "agents": chosen}
    if dry_run:
        return actions
    state_path = safe_path(root, STATE)
    before = {name: (safe_path(root, name).read_bytes() if safe_path(root, name).exists() else None)
              for name in [*writes, *removals, STATE]}
    try:
        # Per-file replacements are atomic; ordinary write failures roll back.
        for name, data in writes.items():
            atomic_write(safe_path(root, name), data)
        for name in removals:
            safe_path(root, name).unlink()
        if uninstall:
            if state_path.exists():
                state_path.unlink()
        else:
            state = {"package": "hard-implementation", "version": RELEASE[1:],
                     "agents": chosen, "files": owned}
            atomic_write(state_path, (json.dumps(state, indent=2) + "\n").encode())
    except OSError:
        for name, data in reversed(list(before.items())):
            path = safe_path(root, name)
            if data is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, data)
        raise
    return actions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", action="append", choices=("codex", "opencode"),
                        help="Repeat to install both; default: both")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--source", type=Path, help="Use a local release checkout (offline)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true", help="Remove only unchanged installer-owned files")
    args = parser.parse_args()
    source = args.source
    if source is None and (Path(__file__).resolve().parent / "distribution.json").is_file():
        source = Path(__file__).resolve().parent
    try:
        result = install(args.project.resolve(), source.resolve() if source else None,
                         args.agent or ["codex", "opencode"], args.dry_run, args.uninstall)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Installation stopped: {exc}\n")
    print(json.dumps(result, indent=2))
    if not args.dry_run and not args.uninstall:
        print("Installed Hard Implementation " + RELEASE)
        if "codex" in result["agents"]:
            print("Codex: $hard-implementation specs/your-feature")
        if "opencode" in result["agents"]:
            print("OpenCode: /hard.implement specs/your-feature")
        print("Restart the agent if the new skill/command is not listed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
