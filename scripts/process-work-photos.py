#!/usr/bin/env python3
"""Process Highland project photos for the public Our Work gallery.

Reads images from /workspace/highland-incoming/ (and any explicit source
paths in work-photos.json). For each photo:

  - auto-orient from EXIF, then strip all EXIF/GPS metadata
  - write a long-edge ~1600px image and a ~600px thumbnail
  - prefer WebP, fall back to JPEG, keep each file under ~300 KB

Unknown files dropped into the incoming folder are processed with a slug
taken from the filename. Add a caption in work-photos.json before putting
them on the site — do not invent client names, places, or dates.

Usage (from the site root):

    python3 scripts/process-work-photos.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path(__file__).resolve().with_name("work-photos.json")
MAX_FULL = 1600
MAX_THUMB = 600
MAX_BYTES = 300 * 1024
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text())


def resolve_source(raw: str, incoming: Path) -> Path:
    p = Path(raw)
    if p.is_absolute():
        return p
    if p.exists():
        return p.resolve()
    cand = (ROOT / p)
    if cand.exists():
        return cand
    return incoming / p.name


def slugify(name: str) -> str:
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return stem or "photo"


def _resize_to_edge(im: Image.Image, long_edge: int) -> Image.Image:
    w, h = im.size
    longest = max(w, h)
    if longest <= long_edge:
        return im
    scale = long_edge / longest
    return im.resize((int(round(w * scale)), int(round(h * scale))), Image.Resampling.LANCZOS)


def save_under_cap(im: Image.Image, dest: Path, max_bytes: int) -> Path:
    """Save as WebP, or JPEG if needed, under max_bytes. Shrinks the long edge if quality alone is not enough."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    candidates = []
    # Prefer a larger image at a moderate quality over a tiny, over-compressed one.
    edges = []
    current = max(im.size)
    for edge in (MAX_FULL if "thumb" not in dest.name else MAX_THUMB, 1400, 1280, 1200, 1000, 800):
        if "thumb" in dest.name:
            edge = min(edge, MAX_THUMB)
        if edge <= current and edge not in edges:
            edges.append(edge)
    qualities_webp = (82, 76, 70, 64, 58, 50)
    qualities_jpeg = (85, 80, 74, 68, 62, 56)
    for edge in edges:
        work = _resize_to_edge(im.convert("RGB"), edge)
        work.info = {}
        for fmt, ext, qualities in (("WEBP", ".webp", qualities_webp), ("JPEG", ".jpg", qualities_jpeg)):
            out = dest.with_suffix(ext)
            for q in qualities:
                kwargs = {"quality": q, "method": 6} if fmt == "WEBP" else {
                    "quality": q,
                    "optimize": True,
                    "progressive": True,
                }
                work.save(out, fmt, **kwargs)
                size = out.stat().st_size
                if size <= max_bytes:
                    # Remove the other format if we wrote both.
                    other = dest.with_suffix(".jpg" if ext == ".webp" else ".webp")
                    if other.exists() and other != out:
                        other.unlink()
                    return out
            candidates.append((size, out))
    # Last resort: keep the smallest file we managed to write.
    candidates.sort()
    if candidates:
        print(f"  warning: {candidates[0][1].name} is {candidates[0][0]} bytes (over {max_bytes})")
        return candidates[0][1]
    raise RuntimeError(f"could not save {dest}")


def prepare(im: Image.Image, long_edge: int) -> Image.Image:
    oriented = ImageOps.exif_transpose(im)
    if oriented.mode not in ("RGB", "L"):
        oriented = oriented.convert("RGB")
    # Rebuild the image so EXIF/GPS and other metadata are not carried over.
    clean = Image.frombytes(oriented.mode, oriented.size, oriented.tobytes())
    clean.info = {}
    return _resize_to_edge(clean, long_edge)


def process_one(src: Path, slug: str, out_dir: Path) -> dict:
    im = Image.open(src)
    full_im = prepare(im, MAX_FULL)
    thumb_im = prepare(im, MAX_THUMB)
    full_path = save_under_cap(full_im, out_dir / slug, MAX_BYTES)
    thumb_path = save_under_cap(thumb_im, out_dir / f"{slug}-thumb", MAX_BYTES)
    with Image.open(full_path) as saved:
        full_size = saved.size
    with Image.open(thumb_path) as saved:
        thumb_size = saved.size
    return {
        "slug": slug,
        "full": str(full_path.relative_to(ROOT)),
        "thumb": str(thumb_path.relative_to(ROOT)),
        "full_size": full_size,
        "thumb_size": thumb_size,
        "full_bytes": full_path.stat().st_size,
        "thumb_bytes": thumb_path.stat().st_size,
    }


def figure_html(entry: dict, processed: dict, featured: bool = False) -> str:
    cls = "work-item featured" if featured else "work-item"
    fw, fh = processed["full_size"]
    tw, th = processed["thumb_size"]
    alt = entry.get("alt") or ""
    caption = entry.get("caption") or ""
    return (
        f'          <figure class="{cls}">\n'
        f'            <button type="button" class="work-zoom js-lightbox"\n'
        f'              data-full="{processed["full"]}"\n'
        f'              data-alt="{alt}"\n'
        f'              data-caption="{caption}"\n'
        f'              aria-label="Enlarge photo: {alt}">\n'
        f'              <img src="{processed["thumb"]}" alt="{alt}" width="{tw}" height="{th}" loading="lazy" decoding="async">\n'
        f'            </button>\n'
        f'            <figcaption>{caption}</figcaption>\n'
        f'          </figure>'
    )


def main() -> int:
    manifest = load_manifest()
    incoming = Path(manifest.get("incoming_dir", "/workspace/highland-incoming"))
    out_dir = ROOT / manifest.get("output_dir", "assets/images/work")
    known = {}
    results = []

    for entry in manifest.get("photos", []):
        src = resolve_source(entry["source"], incoming)
        if not src.exists():
            print(f"skip (missing): {src}")
            continue
        info = process_one(src, entry["slug"], out_dir)
        info.update({k: entry.get(k) for k in ("caption", "alt", "category", "source")})
        results.append((entry, info))
        known[src.resolve()] = True
        print(
            f"ok {entry['slug']}: full {info['full_size']} {info['full_bytes']}B, "
            f"thumb {info['thumb_size']} {info['thumb_bytes']}B -> {info['full']}"
        )

    if incoming.is_dir():
        for path in sorted(incoming.iterdir()):
            if path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            if path.resolve() in known:
                continue
            slug = slugify(path.name)
            info = process_one(path, slug, out_dir)
            print(
                f"ok (unlisted) {path.name} -> {slug}: add a caption in "
                f"scripts/work-photos.json before putting this on the site."
            )
            print(
                f"   full {info['full_size']} {info['full_bytes']}B, "
                f"thumb {info['thumb_size']} {info['thumb_bytes']}B"
            )
            results.append(({"source": path.name, "slug": slug, "caption": "", "alt": ""}, info))

    if results:
        print("\nSuggested gallery markup:\n")
        featured = True
        few = " is-solo" if len(results) == 1 else (" is-few" if len(results) <= 2 else "")
        print(f'        <div class="work-grid{few}">')
        for entry, info in results:
            print(figure_html(entry, info, featured=featured))
            featured = False
        print("        </div>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
