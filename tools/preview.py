#!/usr/bin/env python3
"""Render an isometric contact sheet of every generated head.

Usage:  python3 tools/preview.py   (run tools/build.py first)

Reads the generated geometry and textures from the resource pack, so it
doubles as a check that the UV mapping lines up. Writes docs/heads_preview.png.
"""

import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from mobs import HEADS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RP = ROOT / "packs" / "MobTrophies_RP"
OUT = ROOT / "docs" / "heads_preview.png"

SCALE = 9
CELL_W, CELL_H = 190, 210
COLS = 9

# Camera looks from north-east-above, so the face (north), east side and top show.
F = (-1 / math.sqrt(3), -1 / math.sqrt(3), 1 / math.sqrt(3))
R = (-1 / math.sqrt(2), 0, -1 / math.sqrt(2))
U = (-1 / math.sqrt(6), 2 / math.sqrt(6), 1 / math.sqrt(6))


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def face_quads(cube, tex):
    """Yield (depth, polygon points 3D, rgba) for each visible texel."""
    (x0, y0, z0), (w, h, d) = cube["origin"], cube["size"]
    x1, y1, z1 = x0 + w, y0 + h, z0 + d
    uv = cube["uv"]

    def texel(face, i, j, cols, rows):
        fu, fv = uv[face]["uv"]
        su, sv = uv[face]["uv_size"]
        tu = fu + (i + 0.5) * su / cols
        tv = fv + (j + 0.5) * sv / rows
        return tex.getpixel((int(tu), int(tv)))

    shade = {"north": 0.82, "east": 0.64, "up": 1.0}
    # north face: column 0 at x1 (viewer's left when looking at the face)
    for j in range(h):
        for i in range(w):
            xa, xb = x1 - i, x1 - i - 1
            ya, yb = y1 - j, y1 - j - 1
            pts = [(xa, ya, z0), (xb, ya, z0), (xb, yb, z0), (xa, yb, z0)]
            yield pts, texel("north", i, j, w, h), shade["north"]
    # east face: column 0 at z1
    for j in range(h):
        for i in range(d):
            za, zb = z1 - i, z1 - i - 1
            ya, yb = y1 - j, y1 - j - 1
            pts = [(x1, ya, za), (x1, ya, zb), (x1, yb, zb), (x1, yb, za)]
            yield pts, texel("east", i, j, d, h), shade["east"]
    # top face: row 0 at the back (z1), column 0 at x1
    for j in range(d):
        for i in range(w):
            xa, xb = x1 - i, x1 - i - 1
            za, zb = z1 - j, z1 - j - 1
            pts = [(xa, y1, za), (xb, y1, za), (xb, y1, zb), (xa, y1, zb)]
            yield pts, texel("up", i, j, w, d), shade["up"]


def render(key):
    geo = json.loads((RP / "models" / "blocks" / "heads" / f"{key}_head.geo.json").read_text())
    tex = Image.open(RP / "textures" / "blocks" / "heads" / f"{key}_head.png").convert("RGBA")
    bone = next(b for b in geo["minecraft:geometry"][0]["bones"] if b["name"] == "floor")

    quads = []
    for cube in bone["cubes"]:
        for pts, rgba, s in face_quads(cube, tex):
            cx = sum(p[0] for p in pts) / 4
            cy = sum(p[1] for p in pts) / 4
            cz = sum(p[2] for p in pts) / 4
            quads.append((dot(F, (cx, cy, cz)), pts, rgba, s))
    quads.sort(key=lambda q: -q[0])

    img = Image.new("RGBA", (CELL_W, CELL_H - 30), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    ox, oy = CELL_W / 2, (CELL_H - 30) * 0.72
    for _, pts, rgba, s in quads:
        if rgba[3] == 0:
            continue
        poly = [(ox + dot(R, p) * SCALE, oy - dot(U, p) * SCALE) for p in pts]
        color = tuple(int(c * s) for c in rgba[:3]) + (255,)
        draw.polygon(poly, fill=color)
    return img


def main():
    custom = [h for h in HEADS if not h.vanilla_item]
    rows = math.ceil(len(custom) / COLS)
    sheet = Image.new("RGBA", (COLS * CELL_W, rows * CELL_H), (58, 52, 48, 255))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    for n, head in enumerate(custom):
        cx, cy = (n % COLS) * CELL_W, (n // COLS) * CELL_H
        sheet.alpha_composite(render(head.key), (cx, cy))
        label = head.name.replace(" Head", "").replace(" Skull", "")
        tw = draw.textlength(label, font=font)
        draw.text((cx + (CELL_W - tw) / 2, cy + CELL_H - 30), label, fill=(240, 230, 210), font=font)
    OUT.parent.mkdir(exist_ok=True)
    sheet.convert("RGB").save(OUT)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
