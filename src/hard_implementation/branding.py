"""Terminal wordmarks and specification-system introduction. No image protocol, network or asset dependency."""
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.table import Table

from .core import supported_systems

SIGNATURE_COLOR = "#a855f7"

HARD = (
    "██╗  ██╗ █████╗ ██████╗ ██████╗",
    "██║  ██║██╔══██╗██╔══██╗██╔══██╗",
    "███████║███████║██████╔╝██║  ██║",
    "██╔══██║██╔══██║██╔══██╗██║  ██║",
    "██║  ██║██║  ██║██║  ██║██████╔╝",
    "╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝",
)
SIGNATURE = {
    "A": (" ██ ", "█  █", "████", "█  █", "█  █"),
    "L": ("█   ", "█   ", "█   ", "█   ", "████"),
    "E": ("████", "█   ", "███ ", "█   ", "████"),
    "B": ("███ ", "█  █", "███ ", "█  █", "███ "),
}
BRAND_GRADIENT = ("#28d9e6", "#23bed5", "#329de1", "#4380d8", "#5964c4", "#8352b0")


def wordmark_lines(version):
    lines = [Text("HARD IMPLEMENTATION", style="bold #28d9e6"), Text()]
    lines.extend(Text(row, style="bold " + color) for row, color in zip(HARD, BRAND_GRADIENT))
    lines.append(Text())
    for row in range(5):
        glyphs = " ".join(SIGNATURE[letter][row] for letter in "ALAEEB")
        lines.append(Text(glyphs, style="bold " + SIGNATURE_COLOR))
    lines += [Text("BY ALAEEB", style="bold " + SIGNATURE_COLOR), Text(),
              Text("IMPLEMENT. REVIEW. VERIFY.", style="bold #28d9e6"),
              Text(f"Universal implementation • v{version}", style="dim")]
    return lines


def render_banner(console, version):
    console.print()
    unicode_ok = "utf" in (console.encoding or "").lower()
    if unicode_ok and console.color_system is not None and not console.no_color and console.width >= 40:
        for line in wordmark_lines(version):
            console.print(Align.center(line))
    else:
        compact_labels(console, version, unicode_ok)
    console.print()
    render_systems(console)
    console.print()


def render_systems(console):
    names = supported_systems()
    table = Table.grid(padding=(0, 3))
    table.add_column(overflow="fold")
    if console.width >= 64:
        table.add_column(overflow="fold")
        split = (len(names) + 1) // 2
        for index in range(split):
            right = Text(names[index + split], style="bold cyan") if index + split < len(names) else Text()
            table.add_row(Text(names[index], style="bold cyan"), right)
    else:
        for name in names:
            table.add_row(Text(name, style="bold cyan"))
    console.print(Panel(table, title="[bold cyan]Works with[/bold cyan]", border_style="cyan"))
    console.print(Text("Already using one of these? Implement your ready tasks, review, verify "
                       "and resume progress in your existing workflow.", style="dim"))


def compact_labels(console, version, unicode_ok):
    for label, style in (("HARD IMPLEMENTATION", "bold cyan"), ("BY ALAEEB", "bold " + SIGNATURE_COLOR),
                         ("IMPLEMENT. REVIEW. VERIFY.", "bold cyan")):
        console.print(Align.center(Text(label, style=style)))
    separator = "•" if unicode_ok else "|"
    console.print(Align.center(Text(f"Universal implementation {separator} v{version}", style="dim")))
