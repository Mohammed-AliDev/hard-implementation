# Realistic lion and ALAEEB branding

The [source lion](assets/lion-realistic.png) was generated with the built-in
`image_gen` tool in transparent-background mode. The source pixels/alpha are
preserved here. The terminal displays compiled color cells rather than the
full-resolution bitmap; its apparent detail depends on columns, font and color
support. This is a generated photorealistic image, not a wildlife photograph.

`ALAEEB` uses purple `#a855f7`; HARD retains its cyan/violet gradient. The tagline
is `ROAR. BUILD. VERIFY.`. This visual revision changes no workflow or permissions.

## Source generation prompt

```text
Use case: photorealistic-natural. Asset: realistic roaring lion portrait used as source artwork for a terminal brand banner. Generate a single lifelike adult male African lion head, facing the camera with a slight three-quarter angle, mouth open in a powerful natural roar. Full rounded mane entirely inside the square frame, tightly composed with little empty margin. Realistic golden-brown fur with many fine strands, darker brown layered mane, amber eyes with natural dark pupils, realistic moist dark nose, clearly visible anatomically plausible ivory upper canine teeth, dark mouth and muted pink tongue. High-quality wildlife photography with natural directional light and clear facial structure readable at thumbnail size. Isolated clean cutout with genuinely transparent background including around individual mane hairs; no black/white rectangle. No text, no logo, no glow, no cartoon, no illustration, no polygonal shapes, no pixel art, no exaggerated monster anatomy. Square image, realistic rather than stylized.
```

## Terminal compilation

`scripts/build_lion_art.py` compiles this unchanged source to 36/48/64-column
indexed artwork, using a shared 255-color palette plus transparency. Pillow is
needed only for development compilation. `lion_art.py` stores the source SHA-256
and compressed pixels; the runtime uses base85/zlib and Rich half-block characters.
No image protocol, network download or Pillow installation is needed by users.

- At 104+ columns: 64-column lion beside the wordmarks.
- At 88–103 columns: 48-column lion beside the wordmarks.
- At 75–87 columns: 36-column lion beside the wordmarks.
- At 42–74 columns: centered 36-column lion with compact labels.
- Smaller, monochrome, NO_COLOR or legacy-encoding output uses ASCII/plain labels.

`preview_banner.py` exports the actual renderer at 112 columns by default. Inspect
both background themes and all size thresholds after changes; consistency checks
verify the SVG version and compiled artwork's source hash. The full original
implementation workflow and all security/system references remain preserved.
