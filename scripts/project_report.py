from __future__ import annotations

import json
import sys
from pathlib import Path


FOLDERS = [
    "assets/character",
    "assets/costume",
    "assets/stage",
    "assets/closeups",
    "assets/title",
    "assets/audio",
]


def list_files(folder: Path) -> list[str]:
    if not folder.exists():
        return []
    return sorted(p.name for p in folder.iterdir() if p.is_file() and not p.name.startswith("."))


def main() -> int:
    project = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("projects/untouchable-clone")
    report = {
        "project": str(project),
        "folders": {rel: list_files(project / rel) for rel in FOLDERS},
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

