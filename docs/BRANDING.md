# Glyph lion and ALAEEB branding

The current banner is hand-drawn Unicode text in
`src/hard_implementation/branding.py`. The lion uses block glyphs (`█`, `▄`, `▀`)
and whisker lines, the same large-letter style and cyan/violet gradient as HARD.
Its mane, eyes, muzzle, fangs and open jaw form a roaring lion. ALAEEB stays purple
`#a855f7`; the tagline is `ROAR. BUILD. VERIFY.`.

The lion is 52 columns by 26 rows. It is text artwork, so font and character
support affect its appearance. No image decoding, image protocol, Pillow or asset
download is used. This decorative revision changes no workflow or permissions.

## Terminal layouts

- At 92+ columns: lion beside the HARD/ALAEEB wordmarks.
- At 52–91 columns: centered lion above compact labels.
- Smaller, monochrome, NO_COLOR or legacy-encoding output: ASCII/plain fallback.
- JSON output: no artwork or decoration.

`scripts/preview_banner.py` exports the actual renderer at 112 columns by default.
The SVG uses a monospace font without external downloads. Inspect dark/light and
narrow previews after changes; consistency checks verify the release version and
renderer SHA-256 recorded in the SVG.

## Preserved artwork from v1.3.2

The previous [photorealistic source lion](assets/lion-realistic.png) and its exact
prompt remain preserved for provenance. That image is no longer the active
terminal banner. Its compiler and runtime compressed pixels are available in the
[v1.3.2 source release](https://github.com/Mohammed-AliDev/hard-implementation/releases/tag/v1.3.2).

The image was generated with the built-in `image_gen` tool in transparent-background
mode; its source pixels/alpha are unchanged. It is a generated photorealistic image,
not a wildlife photograph. The historical generation prompt is:

```text
Use case: photorealistic-natural. Asset: realistic roaring lion portrait used as source artwork for a terminal brand banner. Generate a single lifelike adult male African lion head, facing the camera with a slight three-quarter angle, mouth open in a powerful natural roar. Full rounded mane entirely inside the square frame, tightly composed with little empty margin. Realistic golden-brown fur with many fine strands, darker brown layered mane, amber eyes with natural dark pupils, realistic moist dark nose, clearly visible anatomically plausible ivory upper canine teeth, dark mouth and muted pink tongue. High-quality wildlife photography with natural directional light and clear facial structure readable at thumbnail size. Isolated clean cutout with genuinely transparent background including around individual mane hairs; no black/white rectangle. No text, no logo, no glow, no cartoon, no illustration, no polygonal shapes, no pixel art, no exaggerated monster anatomy. Square image, realistic rather than stylized.
```
