"""Export the actual Rich terminal banner as an SVG, without starting setup."""
import argparse
import io
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rich.console import Console
from rich.terminal_theme import TerminalTheme
from hard_implementation import __version__
from hard_implementation.branding import render_banner


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=80)
    parser.add_argument("--theme", choices=("dark", "light"), default="dark")
    args = parser.parse_args()
    if args.width < 20:
        parser.error("Choose a width of at least 20 columns")
    palette = [(0, 0, 0), (180, 40, 40), (40, 160, 90), (220, 160, 40),
               (55, 110, 200), (155, 70, 180), (30, 170, 190), (220, 220, 220)]
    dark = args.theme == "dark"
    theme = TerminalTheme((14, 20, 32) if dark else (246, 248, 250),
                          (217, 225, 240) if dark else (24, 40, 65), palette)
    console = Console(file=io.StringIO(), width=args.width, height=30, record=True,
                      force_terminal=True, color_system="truecolor", no_color=False)
    render_banner(console, __version__)
    svg = console.export_svg(title="HARD IMPLEMENTATION / ALAEEB", theme=theme)
    # Keep the preview self-contained; use the viewer's monospace font.
    svg = re.sub(r"@font-face\s*\{.*?\}", "", svg, flags=re.S)
    svg = "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(svg.encode("utf-8"))
    print(args.output)


if __name__ == "__main__":
    main()
