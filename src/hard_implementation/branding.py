"""Terminal-native lion branding. No image protocol, network or asset dependency."""
from rich.align import Align
from rich.text import Text

PALETTE = {
    ".": "#4c261b", "m": "#a84c1c", "g": "#e58c24", "f": "#ffc96b",
    "y": "#28d9e6", "w": "#fff2cd", "t": "#d85160",
}
# Two pixel rows become one terminal row using upper/lower half blocks.
LION = (
    '                  .                 ',
    '          .      ...      .         ',
    '          ...   ..m..   ...         ',
    '         ..m.....mmm.....m..        ',
    '         g.mmm..mmmmm..mmm.g        ',
    '   .    ..ggmmmmmmmmmmmmmgg..    .  ',
    '   .......mgggmmmmmmmmmgggm.......  ',
    '   ..m......ggggggggggggg......m..  ',
    '    .mmm.....ggggggggggg.....mmm.   ',
    '    .mm...ff.gfffffffffg.ff...mm.   ',
    '    ..m..fffggfffffffffggfff..m..   ',
    '    ..m..ffggfffffffffffggff..m..   ',
    '   ...m..fgggfffffffffffgggf..m...  ',
    ' ....mmm..ggfffffffffffffgg..mmm....',
    '....mmmggg.gfffffffffffffg.gggmmm...',
    ' ..mmggggg....fffffffff....gggggmm..',
    '  ..mggggg.......fff.......gggggm.. ',
    '  ...mgggggyy...fffff...yygggggm... ',
    '   ...gggggggy.yfffffy.yggggggg...  ',
    '   ...gggmggggfffffffffggggmggg...  ',
    '  ...mmgmgggggf.......fgggggmgmm... ',
    '  ...mmgggggwwww.....wwwwgggggmm... ',
    '  ..mmgg...wwwwww...wwwwww...ggmm.. ',
    ' ...ggggggw..wwwww.wwwww..wgggggg...',
    ' ....gggggwwwwwwww.wwwwwwwwggggg....',
    '  ....mg.....wwwwwwwwwww.....gm.... ',
    '   ....mggmgwwwwwwwwwwwwwgmggm....  ',
    '    ....mgmg..www...www..gmgm....   ',
    '     ...mmmg..ww.....ww..gmmm...    ',
    '     ...mmgg...w.....w...ggmm...    ',
    '     ..mgggg...w.ttt.w...ggggm..    ',
    '    ...mmgggg...ttttt...ggggmm...   ',
    '    ......ggg...ttttt...ggg......   ',
    '    .......ggg.wwwwwww.ggg.......   ',
    '         ...gg.wwwwwww.gg...        ',
    '         ....gmmmmmmmmmg....        ',
    '          ...m...mmm...m...         ',
    '          .......mmm.......         ',
    '           .......m.......          ',
    '           .    ..m..    .          ',
    '                 ...                ',
    '                 ...                ',
)

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


def lion_lines():
    lines = []
    for upper, lower in zip(LION[::2], LION[1::2]):
        line = Text()
        for top, bottom in zip(upper, lower):
            if top == bottom == " ":
                line.append(" ")
            elif top == " ":
                line.append("▄", style=PALETTE[bottom])
            elif bottom == " ":
                line.append("▀", style=PALETTE[top])
            else:
                line.append("▀", style=f"{PALETTE[top]} on {PALETTE[bottom]}")
        lines.append(line)
    return lines


def wordmark_lines(version):
    lines = [Text("HARD IMPLEMENTATION", style="bold #28d9e6"), Text()]
    colors = ("#28d9e6", "#23bed5", "#329de1", "#4380d8", "#5964c4", "#8352b0")
    lines.extend(Text(row, style="bold " + color) for row, color in zip(HARD, colors))
    lines.append(Text())
    for row in range(5):
        glyphs = " ".join(SIGNATURE[letter][row] for letter in "ALAEEB")
        lines.append(Text(glyphs, style="bold #e58c24"))
    lines += [Text("BY ALAEEB", style="bold #e58c24"), Text(),
              Text("ROAR. BUILD. VERIFY.", style="bold #28d9e6"),
              Text(f"Universal implementation • v{version}", style="dim")]
    return lines


def render_banner(console, version):
    console.print()
    unicode_ok = "utf" in (console.encoding or "").lower()
    if unicode_ok and console.color_system is not None and not console.no_color and console.width >= 42:
        lion = lion_lines()
        if console.width >= 76:
            words = wordmark_lines(version)
            # Padding keeps both wordmarks intact rather than wrapping the artwork.
            for index, left in enumerate(lion):
                right = words[index] if index < len(words) else Text()
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
    for label, style in (("HARD IMPLEMENTATION", "bold cyan"), ("BY ALAEEB", "bold yellow"),
                         ("ROAR. BUILD. VERIFY.", "bold cyan")):
        console.print(Align.center(Text(label, style=style)))
    separator = "•" if unicode_ok else "|"
    console.print(Align.center(Text(f"Universal implementation {separator} v{version}", style="dim")))
