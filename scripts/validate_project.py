from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = {
    "assets/character": 8,
    "assets/costume": 3,
    "assets/stage": 4,
    "assets/closeups": 6,
    "assets/title": 1,
}


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for p in path.iterdir() if p.is_file() and not p.name.startswith("."))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_project.py <project-dir>")
        return 2

    project = Path(sys.argv[1])
    if not project.exists():
        print(f"Project not found: {project}")
        return 2

    ready = True
    print(f"Validating {project}")
    for rel, minimum in REQUIRED.items():
        folder = project / rel
        count = count_files(folder)
        status = "OK" if count >= minimum else "MISSING"
        print(f"{status:7} {rel:18} {count}/{minimum}")
        ready = ready and count >= minimum

    if ready:
        print("Ready for first-pass video generation.")
        return 0

    print("Not ready. Generate or add the missing assets first.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

