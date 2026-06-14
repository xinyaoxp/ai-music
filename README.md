# AI 音乐 MV 制作套件

这是一个面向学习和复现的本地工程，用来做冷色、未来感、时尚向的 AI 音乐 MV。

目标不是一句神 prompt，而是一条可以重复执行的生产线：

1. 建立稳定的角色资产库。
2. 建立服装、舞台、特写参考图。
3. 先写镜头表，再对着音乐做分镜。
4. 每个镜头单独生成 4 到 5 秒短片。
5. 按节拍剪辑、放大、修补、重做。
6. 记录失败原因，把错误变成规则。

打开 `studio/index.html` 可以看本地工作台。

## 边做边学

先看这些：

1. `lessons/00_learning_path.md`
2. `lessons/01_reference_breakdown.md`
3. `workflow/00_system_overview.md`
4. `workflow/04_second_song_protocol.md`
5. `projects/untouchable-clone/checklists.md`
6. `projects/untouchable-clone/production_log.md`

## 结构

- `projects/untouchable-clone/brief.md` - 创作目标和约束
- `projects/untouchable-clone/shotlist.yaml` - 可复用镜头表
- `projects/untouchable-clone/assets/` - 放生成或上传的素材
- `prompts/` - 角色、场景、视频提示词模板
- `studio/index.html` - 本地学习工作台
- `scripts/validate_project.py` - 检查素材是否够开工

## 基本流程

1. 先读 `projects/untouchable-clone/brief.md`
2. 用 `prompts/01_character_assets.md` 和 `prompts/02_scene_assets.md` 做素材
3. 把结果放进对应素材目录
4. 用 `projects/untouchable-clone/shotlist.yaml` 作为镜头生产清单
5. 每个镜头用 `prompts/03_video_clip_template.md`
6. 用 `projects/untouchable-clone/editing_plan.md` 做剪辑和复盘

## 校验

```powershell
python scripts/validate_project.py projects/untouchable-clone
```

## 资产报告

```powershell
python scripts/project_report.py projects/untouchable-clone
```

## 创建第二首歌项目

```powershell
python scripts/new_song_project.py --slug second-song --title "第二首歌" --duration 36 --style "冷感未来 K-pop 时尚 MV"
```
