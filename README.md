# AI Music MV Production Kit

This workspace is a learning-oriented production kit for making a dark futuristic AI music MV similar in structure to the LibTV canvas reference.

The goal is not one magic prompt. The goal is a repeatable pipeline:

1. Build a consistent character asset library.
2. Build costume, stage, and close-up reference images.
3. Write a shot list against the music.
4. Generate each 4-5 second clip from image references.
5. Upscale, cut, and assemble clips to the beat.
6. Review failures and regenerate weak shots.

Open `studio/index.html` in a browser to view the guided production board.

## Structure

- `projects/untouchable-clone/brief.md` - creative direction and constraints.
- `projects/untouchable-clone/shotlist.yaml` - reusable shot plan.
- `projects/untouchable-clone/assets/` - put generated or uploaded assets here.
- `prompts/` - prompt templates for characters, scenes, and video clips.
- `studio/index.html` - local learning board.
- `scripts/validate_project.py` - checks whether the project has enough assets to begin video generation.

## Basic Workflow

1. Read `projects/untouchable-clone/brief.md`.
2. Generate assets using `prompts/01_character_assets.md` and `prompts/02_scene_assets.md`.
3. Put outputs into the matching asset folders.
4. Use `projects/untouchable-clone/shotlist.yaml` as the clip production checklist.
5. For each shot, use `prompts/03_video_clip_template.md`.
6. Assemble the final edit using the rhythm map in `projects/untouchable-clone/editing_plan.md`.

## Validate

```powershell
python scripts/validate_project.py projects/untouchable-clone
```

