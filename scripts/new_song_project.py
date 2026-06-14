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
  - 歌曲分析
  - 视觉世界
  - 素材库
  - 镜头工厂
  - 剪辑复盘
shots:
{chr(10).join(shots)}
"""


def make_brief(title: str, duration: int, style: str) -> str:
    return f"""# 项目说明：{title}

## 目标

做一支 {duration} 秒的 AI 音乐 MV。

风格方向：

```text
{style}
```

## 成功标准

- MV 能贴合歌曲结构
- 主角保持一致
- 视觉世界统一
- 每个镜头都来自参考图
- 最终剪辑有节奏、有插入镜头、有强开场和强结尾

## 学习目标

做完这个项目后，你应该能解释：

- 每个镜头为什么存在
- 是哪些参考素材在控制它
- prompt 如何把音乐转成图像 / 视频
- 为什么要淘汰某些失败输出
"""


def make_log() -> str:
    return """# 制作记录

## 素材记录

| 日期 | 素材 | 工具 / 模型 | 提示词 | 结果 | 备注 |
| --- | --- | --- | --- | --- | --- |

## 镜头记录

| 镜头 | 候选 | 工具 / 模型 | 参考图 | 结果 | 保留？ | 备注 |
| --- | --- | --- | --- | --- | --- | --- |

## 淘汰记录

| 日期 | 镜头 | 失败类型 | 发生了什么 | 修复方式 |
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
