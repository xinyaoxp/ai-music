from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "external" / "liblib-canvas-assets"
OUT = ROOT / "output" / "liblib-style-cut"
FPS = 24
SIZE = (1280, 720)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def image_files() -> list[Path]:
    files = []
    for p in SRC.iterdir():
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            try:
                im = Image.open(p)
                w, h = im.size
                if w >= 180 and h >= 180:
                    files.append((p, w, h, w * h))
            except Exception:
                pass
    return [x[0] for x in sorted(files, key=lambda x: x[3], reverse=True)]


def load(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def fit_cover(img: Image.Image, size=SIZE, zoom=1.0) -> Image.Image:
    w, h = img.size
    sw, sh = size
    scale = max(sw / w, sh / h) * zoom
    nw, nh = int(w * scale), int(h * scale)
    im = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - sw) // 2
    top = (nh - sh) // 2
    return im.crop((left, top, left + sw, top + sh))


def cold_grade(img: Image.Image, intensity=1.0) -> Image.Image:
    im = ImageEnhance.Contrast(img).enhance(1.32 + 0.22 * intensity)
    im = ImageEnhance.Color(im).enhance(0.66)
    im = ImageEnhance.Brightness(im).enhance(0.96)
    r, g, b = im.split()
    r = ImageEnhance.Brightness(r).enhance(0.84)
    b = ImageEnhance.Brightness(b).enhance(1.22)
    im = Image.merge("RGB", (r, g, b))
    return im


def vignette(img: Image.Image, strength=0.55) -> Image.Image:
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-w * 0.1, -h * 0.35, w * 1.1, h * 1.2), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGB", (w, h), "#020306")
    return Image.composite(img, dark, mask.point(lambda v: int(v * (1 - strength) + 255 * strength)))


def letterbox(img: Image.Image, top=18, bottom=18) -> Image.Image:
    w, h = img.size
    canvas = Image.new("RGB", (w, h), "#020306")
    canvas.paste(img, (0, 0))
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, w, top), fill="#000000")
    d.rectangle((0, h - bottom, w, h), fill="#000000")
    return canvas


def add_light(img: Image.Image, t: float, flash=False) -> Image.Image:
    im = img.copy()
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    w, h = im.size
    x = int(w * (0.15 + 0.7 * ((math.sin(t * 2.7) + 1) / 2)))
    d.polygon([(x - 60, 0), (x + 30, 0), (x + 240, h), (x + 90, h)], fill=(210, 235, 255, 26))
    d.line((0, int(h * 0.18), w, int(h * 0.12)), fill=(180, 210, 255, 26), width=3)
    if flash:
        d.rectangle((0, 0, w, h), fill=(255, 255, 255, 125))
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def add_title(img: Image.Image, text="UnTouchable") -> Image.Image:
    im = img.copy()
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 84)
    except Exception:
        from PIL import ImageFont
        font = ImageFont.load_default()
    w, h = im.size
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    d.text(((w - tw) // 2 + 3, h * 0.08 + 3), text, font=font, fill=(0, 0, 0))
    d.text(((w - tw) // 2, h * 0.08), text, font=font, fill=(230, 235, 240))
    return im


def pick(name: str) -> Path:
    path = SRC / name
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def curate_assets(buckets: dict[str, list[Path]]) -> dict[str, Path]:
    """Hand-curated from the observed LibTV canvas asset bundle.

    The automatic classifier is useful for discovery, but this cut needs direct
    control over shot roles. These files are visible canvas assets copied into
    external/liblib-canvas-assets.
    """
    preferred = {
        "hook": "e7480dd0ade6ffff.png",
        "eyes": "16d2a41de35c8112.png",
        "world": "1ceece822d0b569c.png",
        "world_alt": "2d7d8151a584d7b6.png",
        "performance": "bfbb212ced94ba1a.png",
        "performance_alt": "428f6f3239a3eeb9.png",
        "lips": "013e4fe3d478cc0c.png",
        "texture": "4dc8d17ea6908853.jpg",
        "title": "e59f1014f3edb366.png",
        "final": "0930d339954063c6.png",
        "montage_a": "58c79ce409cc5ad5.png",
        "montage_b": "922182d18f7e900b.png",
    }
    chosen: dict[str, Path] = {}
    for key, filename in preferred.items():
        path = SRC / filename
        if path.exists():
            chosen[key] = path

    fallbacks = {
        "hook": buckets["face"][0],
        "eyes": buckets["face"][0],
        "world": buckets["wide"][0],
        "world_alt": buckets["wide"][1],
        "performance": buckets["full"][0],
        "performance_alt": buckets["full"][1],
        "lips": buckets["face"][1],
        "texture": buckets["stage"][0],
        "title": buckets["title"][0] if buckets["title"] else buckets["wide"][0],
        "final": buckets["title"][1] if len(buckets["title"]) > 1 else buckets["wide"][2],
        "montage_a": buckets["wide"][0],
        "montage_b": buckets["wide"][1],
    }
    for key, fallback in fallbacks.items():
        chosen.setdefault(key, fallback)
    return chosen


def crop_region(img: Image.Image, mode: str) -> Image.Image:
    w, h = img.size
    if mode == "eyes":
        box = (int(w * 0.12), int(h * 0.08), int(w * 0.88), int(h * 0.48))
    elif mode == "lips":
        box = (int(w * 0.16), int(h * 0.30), int(w * 0.84), int(h * 0.76))
    elif mode == "side":
        box = (int(w * 0.08), int(h * 0.05), int(w * 0.72), int(h * 0.92))
    else:
        box = (0, 0, w, h)
    return img.crop(box)


def classify_assets(files: list[Path]) -> dict[str, list[Path]]:
    buckets = {"wide": [], "full": [], "face": [], "title": [], "stage": []}
    for p in files:
        im = load(p)
        w, h = im.size
        ratio = w / max(1, h)
        if ratio > 1.55:
            buckets["wide"].append(p)
        elif h > w * 1.15:
            buckets["full"].append(p)
        else:
            buckets["face"].append(p)
        if w >= 350 and h <= 260:
            buckets["title"].append(p)
    buckets["stage"] = buckets["wide"][3:] or buckets["wide"]
    return buckets


def render_shot(frames: list[Image.Image], asset: Path, duration: float, mode: str, title=False) -> None:
    total = int(duration * FPS)
    base = load(asset)
    for i in range(total):
        t = i / max(1, total - 1)
        zoom = 1.0 + 0.09 * t
        img = base
        if mode in {"eyes", "lips", "side"}:
            img = crop_region(base, mode)
            zoom = 1.2 + 0.18 * t
        elif mode == "pulse":
            zoom = 1.0 + 0.055 * math.sin(t * math.pi * 8)
        elif mode == "snap":
            zoom = 1.12 + 0.16 * (1 - abs(0.5 - t) * 2)
        elif mode == "wide":
            zoom = 1.0 + 0.04 * t
        img = fit_cover(img, zoom=zoom)
        img = cold_grade(img)
        img = add_light(img, t, flash=(i < 3 or (mode in {"pulse", "snap"} and i % 10 < 2)))
        img = vignette(img, 0.30)
        img = letterbox(img, 12, 12)
        if title:
            img = add_title(img)
        frames.append(img)


def render() -> tuple[Path, Path]:
    ensure_dir(OUT)
    files = image_files()
    buckets = classify_assets(files)
    chosen = curate_assets(buckets)
    frames: list[Image.Image] = []
    render_shot(frames, chosen["eyes"], 1.3, "eyes")
    render_shot(frames, chosen["world"], 2.4, "wide", title=True)
    render_shot(frames, chosen["lips"], 1.6, "lips")
    render_shot(frames, chosen["performance"], 2.2, "pulse")
    render_shot(frames, chosen["texture"], 1.0, "snap")
    render_shot(frames, chosen["hook"], 1.5, "side")
    render_shot(frames, chosen["performance_alt"], 1.7, "pulse")
    render_shot(frames, chosen["world_alt"], 2.0, "wide")
    for _ in range(4):
        render_shot(frames, chosen["montage_a"], 0.40, "snap")
        render_shot(frames, chosen["montage_b"], 0.40, "wide")
        render_shot(frames, chosen["eyes"], 0.30, "eyes")
        render_shot(frames, chosen["lips"], 0.30, "lips")
    render_shot(frames, chosen["final"], 2.0, "wide", title=True)

    frame_dir = OUT / "frames"
    ensure_dir(frame_dir)
    for idx, frame in enumerate(frames):
        frame.save(frame_dir / f"frame_{idx:04d}.jpg", quality=92)

    video = OUT / "local_liblib_style_cut.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frame_dir / "frame_%04d.jpg"),
        "-vf", "format=yuv420p",
        "-pix_fmt", "yuv420p",
        str(video),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    contact = OUT / "selected_assets.json"
    contact.write_text(json.dumps({k: str(v) for k, v in chosen.items()}, ensure_ascii=False, indent=2), encoding="utf-8")
    return video, contact


if __name__ == "__main__":
    video_path, manifest_path = render()
    print(video_path)
    print(manifest_path)
