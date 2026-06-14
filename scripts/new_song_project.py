from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
WORKFLOW = ROOT / "workflow"


ASSET_DIRS = [
    "assets/character",
    "assets/costume",
    "assets/stage",
    "assets/closeups",
    "assets/title",
    "assets/audio",
    "clips/raw",
    "clips/selected",
    "edit",
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_shotlist(title: str, duration: int, style: str) -> str:
    unit = max(4, duration // 8)
    shots = []
    for i in range(8):
        start = i * unit
        end = duration if i == 7 else min(duration, (i + 1) * unit)
        shot_id = f"S{i+1:02d}"
        kind = [
            "opening_hook",
            "world_reveal",
            "lip_sync_close_up",
            "performance_medium",
            "insert_detail",
            "side_profile",
            "montage_peak",
            "final_title",
        ][i]
        shots.append(
            f"""  - id: {shot_id}
    seconds: "{start}-{end}"
    type: {kind}
    music_cue: "fill after song analysis"
    references: []
    intent: "fill with the role this shot plays in the song"
    prompt: "Use the visual world: {style}. Fill this prompt after assets exist."
    reject_if:
      - face drift
      - style drift
      - weak motion
      - muddy lighting"""
        )
    return f"""project: {title}
duration_target_seconds: {duration}
style: "{style}"
aspect_ratio: "16:9"
workflow:
  - song_analysis
  - visual_world
  - asset_library
  - shot_factory
  - edit_review
shots:
{chr(10).join(shots)}
"""


def make_brief(title: str, duration: int, style: str) -> str:
    return f"""# Project Brief: {title}

## Target

Create a {duration}-second AI music MV.

Style direction:

```text
{style}
```

## Success Criteria

- The MV fits the song structure.
- The lead character stays consistent.
- The visual world stays coherent.
- Every clip is generated from references.
- The final edit has rhythm, inserts, and strong opening/final images.

## Learning Goal

After finishing this project, you should be able to explain:

- why each shot exists
- which reference assets control it
- how the prompt translates music into image/video
- why weak generations were rejected
"""


def make_log() -> str:
    return """# Production Log

## Asset Log

| Date | Asset | Tool/Model | Prompt | Result | Notes |
| --- | --- | --- | --- | --- | --- |

## Clip Log

| Shot | Candidate | Tool/Model | References | Result | Keep? | Notes |
| --- | --- | --- | --- | --- | --- | --- |

## Rejection Notes

| Date | Shot | Failure Type | What Happened | Repair |
| --- | --- | --- | --- | --- |
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--duration", type=int, default=36)
    parser.add_argument("--style", required=True)
    args = parser.parse_args()

    project = PROJECTS / args.slug
    if project.exists():
        raise SystemExit(f"Project already exists: {project}")

    for rel in ASSET_DIRS:
        (project / rel).mkdir(parents=True, exist_ok=True)

    write(project / "brief.md", make_brief(args.title, args.duration, args.style))
    shutil.copyfile(WORKFLOW / "01_song_analysis_template.md", project / "song_analysis.md")
    shutil.copyfile(WORKFLOW / "02_visual_world_template.md", project / "visual_world.md")
    write(project / "shotlist.yaml", make_shotlist(args.title, args.duration, args.style))
    write(project / "production_log.md", make_log())
    shutil.copyfile(ROOT / "projects" / "untouchable-clone" / "checklists.md", project / "checklists.md")

    print(project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

