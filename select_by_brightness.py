#!/usr/bin/env python3
"""
select_by_brightness.py

Scan a folder of photos, measure brightness, and copy only those
above (or below) a threshold to a destination folder.
"""

import argparse
import csv
import os
import sys
import shutil
from pathlib import Path
from typing import Optional
from PIL import Image, ImageOps

# Supported extensions
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}

def parse_args():
    ap = argparse.ArgumentParser(description="Copy photos meeting a brightness threshold.")
    ap.add_argument("src", type=Path, help="Source folder (scanned recursively)")
    ap.add_argument("dst", type=Path, help="Destination folder")
    ap.add_argument("--threshold", type=float, required=True,
                    help="Brightness threshold (0..255)")
    ap.add_argument("--invert", action="store_true",
                    help="Invert selection (select darker images)")
    return ap.parse_args()

def iter_images(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS:
            yield p

def load_gray(path: Path) -> Optional[Image.Image]:
    try:
        with Image.open(path) as im:
            im = ImageOps.exif_transpose(im)
            return im.convert("L")
    except Exception as e:
        print(f"[WARN] Could not read {path}: {e}", file=sys.stderr)
        return None

def brightness(gray: Image.Image) -> float:
    hist = gray.histogram()
    total = sum(hist)
    return sum(i * c for i, c in enumerate(hist)) / total if total > 0 else 0.0

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def main():
    args = parse_args()
    ensure_dir(args.dst)

    selected = 0
    total = 0
    for path in iter_images(args.src):
        total += 1
        gray = load_gray(path)
        if gray is None:
            continue
        val = brightness(gray)
        is_pick = val >= args.threshold
        if args.invert:
            is_pick = not is_pick

        if is_pick:
            rel = path.relative_to(args.src)
            out_path = args.dst / rel
            ensure_dir(out_path.parent)
            shutil.copy2(path, out_path)
            selected += 1

    print(f"Processed {total} files")
    print(f"Copied {selected} files to {args.dst}")

if __name__ == "__main__":
    main()