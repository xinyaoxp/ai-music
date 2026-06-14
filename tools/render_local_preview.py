from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "local-preview"
ASSET = ROOT / "projects" / "untouchable-clone" / "assets"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\simhei.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, fnt) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=fnt) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def add_grain(img: Image.Image) -> Image.Image:
    px = img.load()
    w, h = img.size
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            n = int(8 * math.sin((x + y) * 0.08))
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return img


def make_scene(size=(1280, 720)) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, "#090a0d")
    d = ImageDraw.Draw(img)
    for y in range(h):
        v = int(8 + 18 * y / h)
        d.line((0, y, w, y), fill=(v, v, v + 4))
    for i in range(7):
        x = int(w * (0.1 + i * 0.13))
        d.line((x, h * 0.2, x + 140, h * 0.95), fill=(100, 110, 120), width=6)
    for i in range(4):
        box = (80 + i * 260, 110 + i * 24, 320 + i * 260, 570 - i * 15)
        d.rounded_rectangle(box, radius=18, outline=(180, 185, 195), width=4)
    img = img.filter(ImageFilter.GaussianBlur(0.3))
    return add_grain(img)


def make_character(pose: str, size=(1280, 720), closeup=False) -> Image.Image:
    w, h = size
    img = make_scene(size)
    d = ImageDraw.Draw(img)
    # spotlight
    d.ellipse((w * 0.28, h * 0.12, w * 0.72, h * 0.86), fill=(20, 20, 24))
    d.ellipse((w * 0.34, h * 0.18, w * 0.66, h * 0.82), outline=(210, 214, 220), width=6)
    # body silhouette
    if closeup:
        d.ellipse((w * 0.38, h * 0.12, w * 0.62, h * 0.36), outline=(230, 232, 240), width=8)
        d.line((w * 0.5, h * 0.36, w * 0.5, h * 0.66), fill=(240, 240, 245), width=10)
        d.line((w * 0.43, h * 0.48, w * 0.58, h * 0.48), fill=(240, 240, 245), width=8)
        d.line((w * 0.47, h * 0.58, w * 0.55, h * 0.58), fill=(240, 240, 245), width=8)
    else:
        d.polygon([(w*0.5, h*0.16), (w*0.57, h*0.27), (w*0.62, h*0.52), (w*0.64, h*0.72), (w*0.36, h*0.72), (w*0.38, h*0.52), (w*0.43, h*0.27)], fill=(225, 228, 236))
        d.rectangle((w*0.44, h*0.28, w*0.56, h*0.48), fill=(30, 30, 34))
        d.line((w*0.36, h*0.34, w*0.25, h*0.54), fill=(220,220,230), width=10)
        d.line((w*0.64, h*0.34, w*0.75, h*0.54), fill=(220,220,230), width=10)
    # face
    d.ellipse((w*0.44, h*0.16, w*0.56, h*0.30), fill=(245, 245, 248))
    d.line((w*0.48, h*0.22, w*0.52, h*0.22), fill=(20, 20, 24), width=3)
    d.line((w*0.505, h*0.22, w*0.535, h*0.22), fill=(20, 20, 24), width=3)
    d.line((w*0.50, h*0.24, w*0.50, h*0.25), fill=(120, 90, 90), width=2)
    d.arc((w*0.475, h*0.25, w*0.525, h*0.275), start=0, end=180, fill=(80, 20, 20), width=2)
    if pose == "eyes-open":
        d.ellipse((w*0.472, h*0.215, w*0.486, h*0.226), fill=(0, 0, 0))
        d.ellipse((w*0.514, h*0.215, w*0.528, h*0.226), fill=(0, 0, 0))
    elif pose == "eyes-closed":
        d.line((w*0.47, h*0.22, w*0.49, h*0.22), fill=(0, 0, 0), width=2)
        d.line((w*0.51, h*0.22, w*0.53, h*0.22), fill=(0, 0, 0), width=2)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    return add_grain(img)


def make_card(title: str, body: str, size=(1280, 720), accent="#8ee6d8") -> Image.Image:
    img = Image.new("RGB", size, "#0d1014")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((36, 36, size[0]-36, size[1]-36), radius=28, fill="#12161b", outline="#2d3440", width=2)
    d.line((80, 92, size[0]-80, 92), fill=accent, width=4)
    tf = font(46)
    bf = font(26)
    d.text((80, 120), title, font=tf, fill="#f4f5f7")
    lines = wrap_text(d, body, size[0]-160, bf)
    y = 214
    for line in lines:
        d.text((80, y), line, font=bf, fill="#b3bac7")
        y += 40
    return add_grain(img)


def save_preview_frames() -> list[Path]:
    ensure_dir(OUT)
    frames: list[Path] = []
    specs = [
        ("S01", make_character("eyes-closed", closeup=True), "眼睛钩子", "闭眼后突然睁开，作为整支 MV 的第一击。"),
        ("S02", make_character("eyes-open"), "舞台揭示", "金属舞台和全身造型先立住世界观。"),
        ("S03", make_card("Lip Sync Close-up", "用近景维持口型和情绪一致性。", accent="#f2cf72"), "口型", "嘴唇特写和音乐卡点。"),
        ("S04", make_scene(), "舞台空间", "冷色金属舞台与高反差光线。"),
        ("S05", make_card("Hands Insert", "短插入镜头负责节奏和遮蔽剪辑缝隙。", accent="#ff8c8c"), "手部", "手部和光束插入。"),
        ("S06", make_character("eyes-open", closeup=True), "侧脸", "侧脸和发丝慢动作。"),
        ("S07", make_card("Fast Montage", "眼睛、嘴唇、手、侧脸、全身，快速切换。", accent="#8ee6d8"), "蒙太奇", "快速蒙太奇。"),
        ("S08", make_card("Final Title", "最后凝视镜头后切黑，出现标题。", accent="#ffffff"), "标题", "最后镜头。"),
    ]
    for i, (_, img, _, _) in enumerate(specs, start=1):
        path = OUT / f"frame_{i:02d}.png"
        img.save(path)
        frames.append(path)
    return frames


def write_contact_sheet(frames: list[Path]) -> Path:
    imgs = [Image.open(p).convert("RGB").resize((320, 180)) for p in frames]
    sheet = Image.new("RGB", (1280, 1080), "#0b0c0e")
    d = ImageDraw.Draw(sheet)
    title_font = font(40)
    small = font(22)
    d.text((40, 28), "AI Music MV Local Preview", font=title_font, fill="#f2f3f5")
    d.text((40, 78), "This proves the local production board and assembly pipeline work end-to-end.", font=small, fill="#a9b0bc")
    for idx, img in enumerate(imgs):
        x = 40 + (idx % 4) * 310
        y = 130 + (idx // 4) * 430
        sheet.paste(img, (x, y))
        d.text((x, y + 192), frames[idx].name, font=small, fill="#8ee6d8")
    out = OUT / "contact_sheet.png"
    sheet.save(out)
    return out


def build_video(frames: list[Path]) -> Path:
    list_file = OUT / "frames.txt"
    with list_file.open("w", encoding="utf-8") as f:
        for p in frames:
            f.write(f"file '{p.as_posix()}'\n")
            f.write("duration 0.75\n")
        f.write(f"file '{frames[-1].as_posix()}'\n")
    out = OUT / "local_preview.mp4"
    import subprocess

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-vf",
        "scale=1280:720,format=yuv420p",
        "-pix_fmt",
        "yuv420p",
        str(out),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out


def main() -> int:
    frames = save_preview_frames()
    contact = write_contact_sheet(frames)
    video = build_video(frames)
    print(contact)
    print(video)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
