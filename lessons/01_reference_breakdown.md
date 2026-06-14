# Reference Breakdown: Why It Works

## Production Pattern

The reference canvas is not a single prompt. It is a node graph.

The graph has five visible layers:

1. Character and identity references.
2. Costume and styling references.
3. Stage and environment images.
4. Short video generation nodes.
5. Utility nodes for crop, upscale, analysis, subtitles, audio, and frame extraction.

## Visual Strategy

The video feels expensive because it repeats a small set of design choices:

- cold monochrome palette
- black/silver costume
- metallic stage geometry
- harsh top light and backlight
- glossy reflections
- intense close-ups
- fast irregular cuts

The viewer experiences variety, but the image system stays consistent.

## Prompt Strategy

The strongest video prompt I observed had this structure:

```text
Epic fashion film, use image 2 as the same performer, preserve the head accessory.
She wears image 1 costume and performs inside image 4 stage while singing to audio 3.
Close-up, accurate lip movement, sexy jazz dance, K-pop, cool camera movement, visual impact.
Cold tone, clear image quality, costume reference image 1.
Include local close-ups of eyes, lips, hands, side face.
Fast irregular cuts, metallic structure surrounds the performer.
Strong top light and backlight, subtle rim glow, ultra realistic, extreme camera movement.
```

Important pattern:

- references control identity and design
- text controls behavior and camera
- short duration keeps quality high
- later editing creates the full music video

## What To Copy

Copy the workflow, not the exact image.

Use:

- reference images for every clip
- 4-5 second clip length
- cold coherent style
- multiple close-up inserts
- strict rejection of failed outputs

Avoid:

- trying to generate a full song at once
- changing style every shot
- relying on text alone for identity
- overexplaining every detail in one prompt

