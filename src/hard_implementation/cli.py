"""Guided project/global setup with honest progress and useful next steps."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

import questionary
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from . import __version__
from .core import bundled_source, installer

AGENTS = {"codex": "Codex", "opencode": "OpenCode", "both": "Codex + OpenCode"}
LOGO = """██╗  ██╗ █████╗ ██████╗ ██████╗
██║  ██║██╔══██╗██╔══██╗██╔══██╗
███████║███████║██████╔╝██║  ██║
██╔══██║██╔══██║██╔══██╗██║  ██║
██║  ██║██║  ██║██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝"""


def banner(console):
    console.print()
    unicode_ok = "utf" in (console.encoding or "").lower()
    if console.width >= 48 and unicode_ok:
        console.print(Align.center(Text(LOGO, style="bold cyan")))
    console.print(Align.center(Text("HARD IMPLEMENTATION", style="bold magenta")))
    console.print(Align.center(Text(f"Complete Spec Kit execution • v{__version__}", style="dim")))
    console.print()


def choose(console, title, choices, default):
    if os.environ.get("TERM") == "dumb":
        console.print(Text(title, style="bold"))
        for number, (label, value) in enumerate(choices, 1):
            console.print(f"  {number}. {label}")
        selected = input("Choose a number: ").strip()
        if not selected:
            return default
        try:
            return choices[int(selected) - 1][1] if int(selected) > 0 else None
        except (ValueError, IndexError):
            raise ValueError("Choose one of the displayed numbers.")
    style = questionary.Style([
        ("qmark", "fg:#00aaaa bold"), ("question", "bold"),
        ("pointer", "fg:#aa55ff bold"), ("highlighted", "fg:#00aaaa bold"),
        ("selected", "fg:#00aaaa"), ("instruction", ""),
    ])
    result = questionary.select(
        title, choices=[questionary.Choice(label, value=value) for label, value in choices],
        default=default, style=style,
        instruction="(Use arrow keys, then Enter)", use_indicator=True,
    ).ask()
    if result is None:
        raise KeyboardInterrupt
    return result


def normalize_agents(values):
    agents = set()
    for value in values or []:
        agents.update(("codex", "opencode") if value == "both" else (value,))
    return sorted(agents)


def configuration_home(root):
    configured = os.environ.get("XDG_CONFIG_HOME")
    return Path(configured).expanduser().resolve() if configured else root / ".config"


def targets(args, console, interactive):
    if args.global_scope and args.path:
        raise ValueError("Use a project path or --global, not both.")
    if args.global_scope:
        scope = "global"
    elif args.here or args.path:
        scope = "project"
    elif interactive:
        scope = choose(console, "Where should the skill be available?", [
            (f"This project  ({Path.cwd()})", "project"),
            ("All my projects on this computer", "global"),
        ], "project")
    else:
        raise ValueError("Choose --here, a project path, or --global. Example: hard init --here --agent both --yes")
    root = Path.home().resolve() if scope == "global" else Path(args.path or Path.cwd()).expanduser().resolve()
    if scope == "project" and str(root).startswith("/path/to/"):
        raise ValueError("That path is an example. In your actual project, run hard init --here.")
    return root, scope


def setup_panel(console, root, scope, agents, dry_run=False):
    info = Table.grid(padding=(0, 2))
    info.add_column(style="dim", no_wrap=True)
    info.add_column(overflow="fold")
    info.add_row("Availability", "All projects on this computer" if scope == "global" else "This project")
    info.add_row("Location", Text(str(root)))
    info.add_row("Coding agents", ", ".join(AGENTS[a] for a in agents))
    info.add_row("Workflow", "Complete original • 2,397 lines • 46 sections")
    if dry_run:
        info.add_row("Mode", "Preview only — no files will be written")
    console.print(Panel(info, title="[bold cyan]Setup[/bold cyan]", border_style="cyan", padding=(1, 2)))


def next_steps(console, root, scope, agents, result, removed=False):
    if removed:
        console.print(Panel(Text("Managed installation removed. Your project files and feature checkpoints were preserved."),
                            title="[bold green]Removed[/bold green]", border_style="green"))
        return
    count = len(result["write"])
    message = Text("Ready to use", style="bold green")
    message.append(f"\n{count} file(s) installed or updated." if count else "\nAlready installed; files verified.", style="")
    message.append("\nThe complete original workflow was preserved and verified.", style="")
    console.print(Panel(message, border_style="green", padding=(1, 2)))
    steps = Text()
    if scope == "global":
        steps.append("1. Open Codex or OpenCode inside the project you want to work on.\n")
    else:
        steps.append("1. Open your coding agent in this project:\n")
        steps.append(f"   {root}\n", style="cyan")
    steps.append("2. In the agent chat, run:\n")
    if "codex" in agents:
        steps.append("   Codex     ", style="bold")
        steps.append("$hard-implementation\n", style="cyan")
    if "opencode" in agents:
        steps.append("   OpenCode  ", style="bold")
        steps.append("/hard.implement\n", style="cyan")
    steps.append("3. If there are multiple Specs, add the actual feature path after the command.\n")
    steps.append("   The feature should already have spec.md, plan.md, and tasks.md.\n")
    steps.append("Restart an already-open agent session if the new skill or command is missing.", style="dim")
    console.print(Panel(steps, title="[bold cyan]Next steps[/bold cyan]", border_style="cyan", padding=(1, 2)))
    console.print("Check installation anytime: [bold]hard status[/bold]")
    console.print()


def inspect(root, scope, config_home):
    path = installer.destination(root, installer.STATE, scope, config_home)
    if not path.exists():
        return {"scope": scope, "root": str(root), "installed": False, "problems": []}
    state = installer.load_state(root, scope, config_home)
    problems = []
    for name, sha in state["files"].items():
        target = installer.destination(root, name, scope, config_home)
        if not target.is_file():
            problems.append(f"Missing: {target}")
        elif hashlib.sha256(target.read_bytes()).hexdigest() != sha:
            problems.append(f"Modified: {target}")
    # Original preservation is checked even when a pre-existing file is unowned.
    original = installer.destination(root, installer.DEST_PREFIX + "references/workflow.md", scope, config_home)
    expected = "3302000990ac049cc068a63927dac29757be8bd8031bb3fb9d5d7c1c715035c7"
    if not original.is_file() or hashlib.sha256(original.read_bytes()).hexdigest() != expected:
        problems.append("The complete original workflow is missing or changed")
    return {"scope": scope, "root": str(root), "installed": True,
            "version": state.get("version"), "agents": state["agents"],
            "problems": problems}


def show_status(args, console):
    if args.path and args.global_scope:
        raise ValueError("Use a project path or --global, not both.")
    home = Path.home().resolve()
    checks = []
    if not args.global_scope:
        root = Path(args.path or Path.cwd()).expanduser().resolve()
        checks.append(inspect(root, "project", None))
    if args.global_scope or (not args.here and not args.path):
        checks.append(inspect(home, "global", configuration_home(home)))
    if args.json:
        print(json.dumps(checks, indent=2))
    else:
        banner(console)
        table = Table(title="Installation status", expand=True, border_style="cyan")
        for column in ("Availability", "Version", "Agents", "Result"):
            table.add_column(column, overflow="fold")
        for result in checks:
            status = "Needs attention" if result["problems"] else ("Verified" if result["installed"] else "Not installed")
            table.add_row("All projects" if result["scope"] == "global" else "This project",
                          result.get("version", "—"), ", ".join(result.get("agents", [])) or "—", status)
            for problem in result["problems"]:
                console.print(Text(problem, style="yellow"))
        console.print(table)
        for result in checks:
            console.print(Text(f"{result['scope']}: {result['root']}", style="dim"))
        console.print("To set up or update: [bold]hard init[/bold]")
    return 1 if any(c["problems"] for c in checks) else 0


def run_setup(args, console):
    interactive = sys.stdin.isatty() and sys.stdout.isatty() and not args.yes and not args.json
    agents = normalize_agents(args.agent)
    if not args.json:
        banner(console)
    if not agents and args.command == "init":
        if not interactive:
            raise ValueError("Choose --agent codex, --agent opencode, or --agent both. Example: hard init --here --agent both --yes")
        detected = [a for a in ("codex", "opencode") if shutil.which(a)]
        default = "both" if len(detected) != 1 else detected[0]
        value = choose(console, "Which coding agent do you use?", [
            ("Codex" + ("  (detected)" if "codex" in detected else ""), "codex"),
            ("OpenCode" + ("  (detected)" if "opencode" in detected else ""), "opencode"),
            ("Both — Codex + OpenCode", "both"),
        ], default)
        agents = normalize_agents([value])
    root, scope = targets(args, console, interactive)
    config_home = configuration_home(root) if scope == "global" else None
    remove = args.command == "uninstall"
    if remove:
        old = installer.load_state(root, scope, config_home)
        if not old["agents"]:
            if args.json:
                print(json.dumps({"installed": False, "scope": scope, "root": str(root)}))
            else:
                console.print(Panel("No managed installation was found at this location.", border_style="yellow"))
            return 0
        agents = old["agents"]
    elif root.is_dir():
        agents = sorted(set(agents) | set(installer.load_state(root, scope, config_home)["agents"]))
    if not args.json:
        setup_panel(console, root, scope, agents, args.dry_run)
    if not args.yes and not args.dry_run:
        if not interactive:
            raise ValueError("Use --yes for non-interactive installation after selecting the scope and agent.")
        approved = questionary.confirm("Remove this installation?" if remove else "Install with these settings?", default=True).ask()
        if approved is None:
            raise KeyboardInterrupt
        if not approved:
            console.print("Cancelled. No files changed.")
            return 0
    created = False
    if not root.exists():
        if remove or scope == "global" or not args.path:
            raise ValueError(f"Directory does not exist: {root}")
        if args.dry_run:
            if args.json:
                print(json.dumps({"would_create_project": str(root), "agents": agents, "scope": scope}))
            else:
                console.print(Text(f"Would create {root} and install the complete skill.", style="cyan"))
            return 0
        root.mkdir(parents=True)
        created = True
    source = args.source.resolve() if args.source else bundled_source()
    tree = Tree("[bold]Remove managed installation[/bold]" if remove else "[bold]Install Hard Implementation[/bold]")
    def progress(stage, detail):
        if stage.endswith("_done"):
            tree.add(Text("✓ " + detail, style="green"))
    try:
        if args.json:
            result = installer.install(root, source, agents, args.dry_run, remove, scope, config_home)
        else:
            with console.status("Verifying workflow and installation…", spinner="dots"):
                result = installer.install(root, source, agents, args.dry_run, remove, scope, config_home, progress)
            console.print(tree)
    except (OSError, ValueError):
        if created and not any(root.iterdir()):
            root.rmdir()
        raise
    if args.json:
        print(json.dumps(result, indent=2))
    elif args.dry_run:
        console.print(Panel(f"Preview: {len(result['write'])} files would be written; {len(result['remove'])} removed.\nNo files changed.",
                            title="Preview", border_style="cyan"))
    else:
        next_steps(console, root, scope, result["agents"], result, remove)
    return 0


def parser():
    result = argparse.ArgumentParser(prog="hard", description="Complete Spec Kit implementation, with guided setup for Codex and OpenCode.")
    result.add_argument("--version", action="version", version=f"Hard Implementation {__version__}")
    commands = result.add_subparsers(dest="command")
    for name, help_text in (("init", "Choose your agent and install into a project or all projects"),
                            ("status", "Verify installed files and show availability"),
                            ("uninstall", "Remove only unchanged installer-owned files")):
        command = commands.add_parser(name, help=help_text, description=help_text)
        command.add_argument("path", nargs="?", help="Project directory; default: current directory")
        scopes = command.add_mutually_exclusive_group()
        scopes.add_argument("--here", action="store_true", help="Use this project")
        scopes.add_argument("--global", dest="global_scope", action="store_true", help="Make available in all projects on this computer")
        command.add_argument("--json", action="store_true", help="Machine-readable output")
        if name != "status":
            command.add_argument("--agent", action="append", choices=("codex", "opencode", "both"))
            command.add_argument("--yes", "-y", action="store_true", help="Non-interactive mode; explicitly choose scope and agent")
            command.add_argument("--dry-run", action="store_true", help="Preview without writing files")
            command.add_argument("--source", type=Path, help="Use a local release checkout (development/offline)")
    return result


def main(argv=None, console=None):
    cli = parser()
    args = cli.parse_args(argv)
    console = console or Console(highlight=False)
    try:
        if args.command is None:
            banner(console)
            cli.print_help()
            console.print("\nStart guided setup: [bold cyan]hard init[/bold cyan]")
            return 0
        return show_status(args, console) if args.command == "status" else run_setup(args, console)
    except KeyboardInterrupt:
        console.print("\nCancelled. No further changes were made.")
        return 130
    except (OSError, ValueError, KeyError, TypeError) as exc:
        if getattr(args, "json", False):
            print(json.dumps({"error": str(exc)}))
        else:
            console.print(Panel(Text(str(exc)), title="[bold red]Setup stopped[/bold red]", border_style="red"))
            console.print("For choices and examples: [bold]hard init --help[/bold]")
        return 1
