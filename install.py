# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Install the complete universal workflow for supported coding agents."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tempfile
from urllib.request import urlopen

REPOSITORY = "Mohammed-AliDev/hard-implementation"
RELEASE = "v1.2.1"
STATE = ".hard-implementation/install.json"
SKILL_PREFIX = "skills/hard-implementation/"
DEST_PREFIX = ".agents/skills/hard-implementation/"
ADAPTER = "adapters/opencode/hard.implement.md"
COMMAND = ".opencode/commands/hard.implement.md"
GLOBAL_STATE = ".hard-implementation/global-install.json"

# Commands load the canonical skill; its standard-compliant name stays unchanged.
COMMAND_ADAPTERS = {
    "opencode": (ADAPTER, COMMAND),
    "claude": ("adapters/claude/hard.implement.md", ".claude/commands/hard.implement.md"),
    "commandcode": ("adapters/commandcode/hard.implement.md", ".commandcode/commands/hard.implement.md"),
    "pi": ("adapters/pi/hard.implement.md", ".pi/prompts/hard.implement.md"),
    "vscode": ("adapters/vscode/hard.implement.prompt.md", ".github/prompts/hard.implement.prompt.md"),
}
COMMAND_NAMES = {target for _, target in COMMAND_ADAPTERS.values()}
VSCODE_COMMAND = COMMAND_ADAPTERS["vscode"][1]
PI_COMMAND = COMMAND_ADAPTERS["pi"][1]

# Native skill discovery; hosts sharing .agents need no duplicate copy.
AGENTS = {
    "codex": {"label": "Codex", "command": "$hard-implementation", "cli": "codex"},
    "opencode": {"label": "OpenCode", "command": "/hard.implement", "cli": "opencode"},
    "claude": {"label": "Claude Code", "command": "/hard.implement", "cli": "claude"},
    "hermes": {"label": "Hermes", "command": "/hard-implementation", "cli": "hermes"},
    "commandcode": {"label": "Command Code", "command": "/hard.implement", "cli": "cmd"},
    "zcode": {"label": "ZCode", "command": "$hard-implementation", "cli": "zcode"},
    "antigravity": {"label": "Antigravity", "command": "/hard-implementation", "cli": "agy"},
    "warp": {"label": "Warp", "command": "/hard-implementation", "cli": "warp"},
    "pi": {"label": "Pi", "command": "/hard.implement", "cli": "pi"},
    "vscode": {"label": "VS Code / GitHub Copilot", "command": "/hard.implement", "cli": "code"},
}
NATIVE_PREFIXES = (
    ".claude/skills/hard-implementation/", ".zcode/skills/hard-implementation/",
    ".hermes/skills/hard-implementation/", ".gemini/config/skills/hard-implementation/",
    ".gemini/antigravity-cli/skills/hard-implementation/",
)


def skill_prefixes(agents, scope="project"):
    prefixes = [DEST_PREFIX]
    for agent in agents:
        if agent == "claude":
            prefixes.append(NATIVE_PREFIXES[0])
        if agent == "zcode":
            prefixes.append(NATIVE_PREFIXES[1])
        if scope == "global" and agent == "hermes":
            prefixes.append(NATIVE_PREFIXES[2])
        if scope == "global" and agent == "antigravity":
            prefixes.extend(NATIVE_PREFIXES[3:])
    return sorted(set(prefixes))



def destination(root, name, scope="project", config_home=None, hermes_home=None):
    if scope not in ("project", "global"):
        raise ValueError("Invalid installation scope")
    if scope == "global" and name == STATE:
        return safe_path(root, GLOBAL_STATE)
    if scope == "global" and name == COMMAND:
        config = Path(config_home) if config_home is not None else root / ".config"
        if not config.is_absolute():
            raise ValueError("OpenCode configuration directory must be absolute")
        if config.is_symlink():
            raise ValueError(f"Refusing symlink configuration directory: {config}")
        return safe_path(config, "opencode/commands/hard.implement.md")
    if scope == "global" and name == PI_COMMAND:
        return safe_path(root, ".pi/agent/prompts/hard.implement.md")
    if scope == "global" and name == VSCODE_COMMAND:
        # VS Code Stable's default user profile; no settings/profile changes.
        if sys.platform == "win32":
            return safe_path(root, "AppData/Roaming/Code/User/prompts/hard.implement.prompt.md")
        if sys.platform == "darwin":
            return safe_path(root, "Library/Application Support/Code/User/prompts/hard.implement.prompt.md")
        config = Path(config_home) if config_home is not None else root / ".config"
        if not config.is_absolute() or config.is_symlink():
            raise ValueError("VS Code configuration directory must be absolute and not a symlink")
        return safe_path(config, "Code/User/prompts/hard.implement.prompt.md")
    if scope == "global" and name.startswith(NATIVE_PREFIXES[2]) and hermes_home is not None:
        home = Path(hermes_home)
        if not home.is_absolute() or home.is_symlink():
            raise ValueError("Hermes home must be an absolute non-symlink directory")
        return safe_path(home, name[len(".hermes/"):])
    return safe_path(root, name)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def valid_relative(name):
    return (isinstance(name, str) and bool(name) and "\\" not in name
            and ":" not in name and not name.startswith("/")
            and all(p not in ("", ".", "..") for p in name.split("/")))


def managed_name(name):
    return valid_relative(name) and (any(name.startswith(prefix) for prefix in (DEST_PREFIX, *NATIVE_PREFIXES)) or name in COMMAND_NAMES)


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


def load_state(root, scope="project", config_home=None, hermes_home=None):
    path = destination(root, STATE, scope, config_home, hermes_home)
    if not path.exists():
        return {"files": {}, "agents": []}
    state = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(state, dict) or state.get("package") != "hard-implementation":
        raise ValueError("Unrecognized installation record")
    if state.get("scope", "project") != scope:
        raise ValueError("Installation record belongs to another scope")
    if scope == "global" and COMMAND in state.get("files", {}):
        expected = str(destination(root, COMMAND, scope, config_home))
        if state.get("command_path") != expected:
            raise ValueError("OpenCode configuration location changed; use the recorded location to manage this installation")
    if not isinstance(state.get("files"), dict) or not isinstance(state.get("agents"), list):
        raise ValueError("Invalid installation record")
    if any(a not in AGENTS for a in state["agents"]):
        raise ValueError("Invalid agent in installation record")
    if not isinstance(state.get("external_paths", {}), dict):
        raise ValueError("Invalid external installation paths")
    for name, saved_path in state.get("external_paths", {}).items():
        if name not in state["files"] or str(destination(root, name, scope, config_home, hermes_home)) != saved_path:
            raise ValueError("External configuration location changed; restore the recorded location before managing this installation")
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


def payload(source, agents, scope="project"):
    manifest = json.loads(read_source(source, "distribution.json"))
    if manifest.get("package") != "hard-implementation" or manifest.get("version") != RELEASE[1:]:
        raise ValueError("Wrong package or release in distribution manifest")
    files = manifest.get("files")
    if not isinstance(files, dict) or SKILL_PREFIX + "SKILL.md" not in files:
        raise ValueError("Incomplete distribution manifest")
    required = ["references/workflow.md", "references/execution.md",
                "assets/implementation-state.md", "scripts/audit_tasks.py",
                "references/systems.md", "scripts/discover_system.py"]
    if (any(SKILL_PREFIX + name not in files for name in required)
            or any(adapter not in files for adapter, _ in COMMAND_ADAPTERS.values())):
        raise ValueError("Required workflow resources or adapter missing")
    adapters = {adapter: (agent, target) for agent, (adapter, target) in COMMAND_ADAPTERS.items()}
    result = {}
    for name, sha in files.items():
        if not valid_relative(name):
            raise ValueError("Invalid source path in distribution manifest")
        if name.startswith(SKILL_PREFIX):
            destinations = [prefix + name[len(SKILL_PREFIX):] for prefix in skill_prefixes(agents, scope)]
        elif name in adapters:
            agent, target = adapters[name]
            if agent not in agents:
                continue
            destinations = [target]
        else:
            raise ValueError(f"Unexpected package resource: {name}")
        data = read_source(source, name)
        if digest(data) != sha:
            raise ValueError(f"Checksum mismatch: {name}")
        for target in destinations:
            result[target] = data
    return result


def install(root, source, agents, dry_run=False, uninstall=False,
            scope="project", config_home=None, on_event=None, hermes_home=None):
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")
    notify = on_event or (lambda stage, detail: None)
    path_for = lambda name: destination(root, name, scope, config_home, hermes_home)
    old = load_state(root, scope, config_home, hermes_home)
    chosen = sorted(set(agents) | set(old["agents"]))
    if not set(chosen) <= set(AGENTS) or (not chosen and not uninstall):
        raise ValueError("Choose at least one supported coding agent")
    notify("workflow", "Loading the complete workflow")
    desired = {} if uninstall else payload(source, chosen, scope)
    if scope == "global" and COMMAND in desired:
        skill_path = str(path_for(DEST_PREFIX + "SKILL.md"))
        desired[COMMAND] = desired[COMMAND].replace(
            b".agents/skills/hard-implementation/SKILL.md", skill_path.encode("utf-8"))
    skill_path = (path_for(DEST_PREFIX + "SKILL.md").as_posix() if scope == "global"
                  else DEST_PREFIX + "SKILL.md")
    for name in COMMAND_NAMES - {COMMAND}:
        if name in desired:
            desired[name] = desired[name].replace(
                b"{{HARD_SKILL_PATH}}", json.dumps(skill_path, ensure_ascii=False).encode("utf-8"))
    notify("workflow_done", "Full workflow and resources verified")
    owned = {}
    writes, removals = {}, []
    # Preflight the entire operation before modifying any destination.
    for name in sorted(set(old["files"]) | set(desired)):
        path = path_for(name)
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
    notify("preflight_done", "Existing files checked and protected")
    actions = {"write": sorted(writes), "remove": removals, "agents": chosen,
               "scope": scope, "destinations": {name: str(path_for(name)) for name in desired},
               "version": RELEASE[1:]}
    if dry_run:
        return actions
    state_path = path_for(STATE)
    before = {name: (path_for(name).read_bytes() if path_for(name).exists() else None)
              for name in [*writes, *removals, STATE]}
    try:
        # Per-file replacements are atomic; ordinary write failures roll back.
        for name, data in writes.items():
            atomic_write(path_for(name), data)
        for name in removals:
            path_for(name).unlink()
        notify("write_done", "Files removed" if uninstall else "Skill and selected commands installed")
        for name, data in desired.items():
            if digest(path_for(name).read_bytes()) != digest(data):
                raise ValueError(f"Installed file verification failed: {path_for(name)}")
        if uninstall:
            if state_path.exists():
                state_path.unlink()
        else:
            state = {"package": "hard-implementation", "version": RELEASE[1:],
                     "agents": chosen, "files": owned, "scope": scope}
            if scope == "global":
                state["command_path"] = str(path_for(COMMAND))
            state["external_paths"] = {name: str(path_for(name)) for name in owned
                                       if name in COMMAND_NAMES or (scope == "global" and name.startswith(NATIVE_PREFIXES[2]))}
            atomic_write(state_path, (json.dumps(state, indent=2) + "\n").encode())
    except (OSError, ValueError):
        for name, data in reversed(list(before.items())):
            path = path_for(name)
            if data is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, data)
        raise
    notify("verify_done", "Installed files verified" if not uninstall else "Managed installation removed")
    return actions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", action="append", choices=tuple(AGENTS),
                        help="Repeat to select agents; default: Codex and OpenCode")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--source", type=Path, help="Use a local release checkout (offline)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true", help="Remove only unchanged installer-owned files")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args()
    if str(args.project).startswith("/path/to/"):
        parser.error("That is an example path. From your project folder, omit --project or use --project .")
    source = args.source
    if source is None and (Path(__file__).resolve().parent / "distribution.json").is_file():
        source = Path(__file__).resolve().parent
    try:
        result = install(args.project.resolve(), source.resolve() if source else None,
                         args.agent or ["codex", "opencode"], args.dry_run, args.uninstall)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Installation stopped: {exc}\n")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Project: {args.project.resolve()}")
        print(f"Files written: {len(result['write'])}; removed: {len(result['remove'])}")
    if not args.json and not args.dry_run and not args.uninstall:
        print("Installed Hard Implementation " + RELEASE)
        for agent in result["agents"]:
            print(f"{AGENTS[agent]['label']}: {AGENTS[agent]['command']}")
        print("Restart the agent if the new skill/command is not listed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
