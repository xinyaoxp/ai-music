# Second Song Protocol

Use this when starting a new song.

## Step 1: Create A New Project

```powershell
python scripts/new_song_project.py --slug my-song --title "My Song" --duration 36 --style "cold futuristic K-pop fashion MV"
```

If the system `python` does not work on Windows, use the bundled runtime path:

```powershell
& "C:\Users\chenjingxian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\new_song_project.py --slug my-song --title "My Song" --duration 36 --style "cold futuristic K-pop fashion MV"
```

## Step 2: Fill Song Analysis

Edit:

```text
projects/<slug>/song_analysis.md
```

Do not make assets until this is filled.

## Step 3: Define Visual World

Edit:

```text
projects/<slug>/visual_world.md
```

The world must be specific enough that every shot belongs to it.

## Step 4: Build Assets

Put files into:

```text
projects/<slug>/assets/character
projects/<slug>/assets/costume
projects/<slug>/assets/stage
projects/<slug>/assets/closeups
projects/<slug>/assets/title
projects/<slug>/assets/audio
```

## Step 5: Generate Clips

Use:

```text
projects/<slug>/shotlist.yaml
projects/<slug>/production_log.md
```

Generate at least two candidates per shot.

## Step 6: Edit And Repair

Use the rejection log. Keep the system, change the shots.

