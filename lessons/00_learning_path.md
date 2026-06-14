# Learning Path

This project is designed as a watch-and-build course. Do not skip stages.

## Stage 1: Read The Reference Like A Director

Goal: understand why the reference looks expensive.

Look for:

- repeated face identity
- repeated costume language
- repeated color and lighting
- short clips instead of long scenes
- close-up inserts for rhythm
- strong stage silhouette
- aggressive rejection of weak outputs

Deliverable:

- one paragraph describing the target style in your own words
- a list of 8 shot ideas

## Stage 2: Build The Asset Library

Goal: make the model stop inventing a new film every time.

Create:

- identity sheet
- costume references
- stage references
- close-up insert references
- title/logo reference

Deliverable:

- put files into `projects/untouchable-clone/assets/`
- run `python scripts/validate_project.py projects/untouchable-clone`

## Stage 3: Generate First-Pass Clips

Goal: produce usable 4-5 second clips.

Rules:

- one shot per generation task
- always use image references
- keep prompts specific but not overloaded
- generate multiple candidates per shot
- reject ugly clips quickly

Deliverable:

- at least 2 candidates per shot
- fill `projects/untouchable-clone/production_log.md`

## Stage 4: Edit To Music

Goal: make the generated clips feel intentional.

Rules:

- cut on rhythm
- use inserts to hide weak transitions
- keep the color grade unified
- do not keep a weak shot because it cost credits

Deliverable:

- 30-45 second first cut
- a list of clips to regenerate

## Stage 5: Repair And Polish

Goal: turn a promising AI test into a finished short.

Repair:

- face drift
- costume drift
- bad hands
- weak motion
- muddy lighting
- bad lip sync

Deliverable:

- final render
- a written postmortem explaining what worked

