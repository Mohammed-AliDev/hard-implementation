# HARD / ALAEEB and specification systems

The current banner displays the HARD wordmark, a purple ALAEEB signature and
`IMPLEMENT. REVIEW. VERIFY.`. It contains no lion or other animal artwork.
`src/hard_implementation/branding.py` renders the lettering and the system panel.

Immediately below the brand, the `Works with` panel displays **Spec Kit, Kiro Specs,
cc-sdd, Spec Workflow MCP, OpenSpec, Spec Kitty, Conductor and Superpowers**. A short
explanation says that Hard Implementation executes ready tasks, reviews, verifies
and resumes progress using the project's existing specification workflow.

The system names come from `project-metadata.json`, included in the installed
package and also used to generate GitHub About and the README/skill opening blocks.
This avoids independent, stale copies of the supported-system list.

## Terminal layouts

- At 40+ columns with color/UTF support: HARD and ALAEEB block lettering.
- Narrow, monochrome, NO_COLOR or legacy-encoding output: compact plain labels.
- The systems panel uses two columns at 64+ columns and one column otherwise.
- JSON output: no banner or panel decoration.

`scripts/preview_banner.py` exports the actual renderer at 112 columns by default.
The SVG uses a monospace font without external downloads. Inspect dark/light and
narrow previews after changes; consistency checks verify the release version and
renderer/registry SHA-256 recorded in the SVG.

## Previous glyph artwork

The lion glyphs were removed from the current banner at the author's request.
They remain in the [v1.3.3 source release](https://github.com/Mohammed-AliDev/hard-implementation/releases/tag/v1.3.3).

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
