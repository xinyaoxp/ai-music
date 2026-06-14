# 第二首歌迁移协议

新歌开始时就用这个。

## 第 1 步：创建新项目

```powershell
python scripts/new_song_project.py --slug my-song --title "我的歌" --duration 36 --style "冷感未来 K-pop 时尚 MV"
```

如果系统 `python` 在 Windows 上不可用，就用内置运行时：

```powershell
& "C:\Users\chenjingxian\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\new_song_project.py --slug my-song --title "我的歌" --duration 36 --style "冷感未来 K-pop 时尚 MV"
```

## 第 2 步：填写歌曲分析

编辑：

```text
projects/<slug>/song_analysis.md
```

没填完之前不要做素材。

## 第 3 步：定义视觉世界

编辑：

```text
projects/<slug>/visual_world.md
```

这个世界必须足够具体，保证每个镜头都属于它。

## 第 4 步：做素材

把文件放进：

```text
projects/<slug>/assets/character
projects/<slug>/assets/costume
projects/<slug>/assets/stage
projects/<slug>/assets/closeups
projects/<slug>/assets/title
projects/<slug>/assets/audio
```

## 第 5 步：生成镜头

使用：

```text
projects/<slug>/shotlist.yaml
projects/<slug>/production_log.md
```

每个镜头至少做两个候选。

## 第 6 步：剪辑和修复

看淘汰记录。系统别变，镜头可以改。
