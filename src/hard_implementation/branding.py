"""Terminal-native lion branding. No image protocol, network or asset dependency."""
from rich.align import Align
from rich.text import Text

from base64 import b85decode
from functools import lru_cache
import zlib

from .lion_art import IMAGES, PALETTE

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
ASCII_LION = (
    "       ,wWWWw,",
    "    ,W'  ^ ^  'W,",
    "   W  ( o   o )  W",
    r"  W  /  .-v-.  \  W",
    "  W  |  |^ ^|  |  W",
    r"   W  \ |___| /  W",
    "    'Ww._____.wW'",
)


@lru_cache(maxsize=3)
def lion_lines(size):
    pixels = zlib.decompress(b85decode(IMAGES[size]))
    lines = []
    for y in range(0, size, 2):
        line = Text()
        for x in range(size):
            top, bottom = pixels[y * size + x], pixels[(y + 1) * size + x]
            if top == bottom == 0:
                line.append(" ")
            elif top == 0:
                line.append("▄", style=PALETTE[bottom])
            elif bottom == 0:
                line.append("▀", style=PALETTE[top])
            else:
                line.append("▀", style=f"{PALETTE[top]} on {PALETTE[bottom]}")
        lines.append(line)
    return tuple(lines)


def wordmark_lines(version):
    lines = [Text("HARD IMPLEMENTATION", style="bold #28d9e6"), Text()]
    colors = ("#28d9e6", "#23bed5", "#329de1", "#4380d8", "#5964c4", "#8352b0")
    lines.extend(Text(row, style="bold " + color) for row, color in zip(HARD, colors))
    lines.append(Text())
    for row in range(5):
        glyphs = " ".join(SIGNATURE[letter][row] for letter in "ALAEEB")
        lines.append(Text(glyphs, style="bold " + SIGNATURE_COLOR))
    lines += [Text("BY ALAEEB", style="bold " + SIGNATURE_COLOR), Text(),
              Text("ROAR. BUILD. VERIFY.", style="bold #28d9e6"),
              Text(f"Universal implementation • v{version}", style="dim")]
    return lines


def render_banner(console, version):
    console.print()
    unicode_ok = "utf" in (console.encoding or "").lower()
    if unicode_ok and console.color_system is not None and not console.no_color and console.width >= 42:
        size = 64 if console.width >= 104 else (48 if console.width >= 88 else 36)
        lion = lion_lines(size)
        if console.width >= size + 39:
            words = wordmark_lines(version)
            # Padding keeps both wordmarks intact rather than wrapping the artwork.
            offset = max(0, (len(lion) - len(words)) // 2)
            for index, left in enumerate(lion):
                word_index = index - offset
                right = words[word_index].copy() if 0 <= word_index < len(words) else Text()
                right.align("center", 36)
                line = Text.assemble(left, "   ", right)
                console.print(Align.center(line), soft_wrap=True)
        else:
            for line in lion:
                console.print(Align.center(line), soft_wrap=True)
            compact_labels(console, version, unicode_ok)
    else:
        if console.width >= 24:
            for line in ASCII_LION:
                console.print(Align.center(Text(line, style="bold yellow")), soft_wrap=True)
        compact_labels(console, version, unicode_ok)
    console.print()


def compact_labels(console, version, unicode_ok):
    for label, style in (("HARD IMPLEMENTATION", "bold cyan"), ("BY ALAEEB", "bold " + SIGNATURE_COLOR),
                         ("ROAR. BUILD. VERIFY.", "bold cyan")):
        console.print(Align.center(Text(label, style=style)))
    separator = "•" if unicode_ok else "|"
    console.print(Align.center(Text(f"Universal implementation {separator} v{version}", style="dim")))
