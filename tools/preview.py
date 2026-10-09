#!/usr/bin/env python3
"""Render contact sheets of the generated heads.

Usage:  python3 tools/preview.py                (run tools/build.py first)
        python3 tools/preview.py --only cat,cow --back --out /tmp/cats.png

Reads the generated geometry and textures from the resource pack, so it
doubles as a check that the UV mapping lines up. By default writes
docs/heads_preview.png (every head, seen from the front) and
docs/worn_preview.png (a few heads worn by a player).

  --only a,b   only mobs whose key starts with one of these (variants included)
  --back       add a second view of each head from behind
  --worn       render the worn model on a player instead of the placed block
  --out PATH   where to write the sheet
  --zoom N     draw each head N times bigger (handy for checking detail)
"""

import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from mobs import HEADS, trophies  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RP = ROOT / "dist" / "MobTrophies_RP"
OUT = ROOT / "docs" / "heads_preview.png"
WORN_OUT = ROOT / "docs" / "worn_preview.png"
WORN_SHOWCASE = ["cow", "chicken", "cat_tuxedo", "fox", "villager_desert", "witch",
                 "axolotl_blue", "enderman", "frog", "iron_golem", "panda", "sheep_lime"]

COLS = 10
CELL_W, CELL_H = 170, 200
LABEL_H = 34

# Each face, seen from outside: (corner of texel (0, 0), step right, step down),
# for a box from (x0, y0, z0) to (x1, y1, z1). See tools/mobs.py for how art
# maps onto faces; this mirrors what the game does.
FACE_FRAMES = {
    "north": (lambda b: (b[3], b[4], b[2]), (-1, 0, 0), (0, -1, 0)),
    "south": (lambda b: (b[0], b[4], b[5]), (1, 0, 0), (0, -1, 0)),
    "east": (lambda b: (b[3], b[4], b[5]), (0, 0, -1), (0, -1, 0)),
    "west": (lambda b: (b[0], b[4], b[2]), (0, 0, 1), (0, -1, 0)),
    "up": (lambda b: (b[3], b[4], b[5]), (-1, 0, 0), (0, 0, -1)),
}
NORMALS = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0),
           "west": (-1, 0, 0), "up": (0, 1, 0)}
LIGHT = {"north": 0.86, "south": 0.7, "east": 0.68, "west": 0.6, "up": 1.0}


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def camera(yaw_deg):
    """Forward, right and up vectors for a camera above the model.

    yaw 0 looks at the face from the front-right (showing the north face,
    the east side and the top); yaw 180 looks at the back.
    """
    yaw = math.radians(yaw_deg)
    # Camera position direction (from the model towards the camera).
    pos = (math.sin(yaw + math.pi / 4) * 1, 1.0, -math.cos(yaw + math.pi / 4) * 1)
    n = math.sqrt(dot(pos, pos))
    fwd = tuple(-p / n for p in pos)
    up0 = (0, 1, 0)
    right = (fwd[1] * up0[2] - fwd[2] * up0[1], fwd[2] * up0[0] - fwd[0] * up0[2],
             fwd[0] * up0[1] - fwd[1] * up0[0])
    rn = math.sqrt(dot(right, right))
    right = tuple(r / rn for r in right)
    up = (right[1] * fwd[2] - right[2] * fwd[1], right[2] * fwd[0] - right[0] * fwd[2],
          right[0] * fwd[1] - right[1] * fwd[0])
    return fwd, right, up


def quads_for(cube, tex, fwd, color=None):
    (x0, y0, z0), (w, h, d) = cube["origin"], cube["size"]
    box = (x0, y0, z0, x0 + w, y0 + h, z0 + d)
    for face, (corner, rstep, dstep) in FACE_FRAMES.items():
        if dot(NORMALS[face], fwd) >= 0:
            continue  # facing away from the camera
        span_r = {"north": w, "south": w, "east": d, "west": d, "up": w}[face]
        span_d = {"north": h, "south": h, "east": h, "west": h, "up": d}[face]
        if color is not None:
            cols, rows = 1, 1
        else:
            fu, fv = cube["uv"][face]["uv"]
            su, sv = cube["uv"][face]["uv_size"]
            cols, rows = max(1, round(abs(su))), max(1, round(abs(sv)))
        c0 = corner(box)
        for j in range(rows):
            for i in range(cols):
                a0, a1 = span_r * i / cols, span_r * (i + 1) / cols
                b0, b1 = span_d * j / rows, span_d * (j + 1) / rows

                def p(a, b):
                    return tuple(c0[k] + rstep[k] * a + dstep[k] * b for k in range(3))

                pts = [p(a0, b0), p(a1, b0), p(a1, b1), p(a0, b1)]
                if color is not None:
                    rgba = color
                else:
                    tu = fu + (i + 0.5) * su / cols
                    tv = fv + (j + 0.5) * sv / rows
                    rgba = tex.getpixel((min(tex.width - 1, int(tu)), min(tex.height - 1, int(tv))))
                yield pts, rgba, LIGHT[face]


def draw_model(parts, size, yaw=0, scale=None, margin=10):
    """parts: list of (cubes, texture or None, solid colour or None)."""
    fwd, right, up = camera(yaw)
    quads = []
    for cubes, tex, color in parts:
        for cube in cubes:
            for pts, rgba, light in quads_for(cube, tex, fwd, color):
                c = tuple(sum(p[k] for p in pts) / 4 for k in range(3))
                quads.append((dot(fwd, c), pts, rgba, light))
    quads.sort(key=lambda q: -q[0])
    proj = [[(dot(right, p), dot(up, p)) for p in q[1]] for q in quads]
    xs = [x for pr in proj for x, _ in pr] or [0]
    ys = [y for pr in proj for _, y in pr] or [0]
    w, h = size
    if scale is None:
        scale = min((w - 2 * margin) / max(1e-6, max(xs) - min(xs)),
                    (h - 2 * margin) / max(1e-6, max(ys) - min(ys)), 12 * w / 170)
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for (_, _, rgba, light), pr in zip(quads, proj):
        if rgba[3] == 0:
            continue
        poly = [(w / 2 + (x - cx) * scale, h / 2 - (y - cy) * scale) for x, y in pr]
        color = tuple(int(c * light) for c in rgba[:3]) + (255,)
        draw.polygon(poly, fill=color, outline=color)
    return img


def load(key, worn=False):
    if worn:
        geo_path = RP / "models" / "entity" / "heads" / f"{key}_head.worn.geo.json"
    else:
        geo_path = RP / "models" / "blocks" / "heads" / f"{key}_head.geo.json"
    geo = json.loads(geo_path.read_text())
    tex = Image.open(RP / "textures" / "blocks" / "heads" / f"{key}_head.png").convert("RGBA")
    bones = geo["minecraft:geometry"][0]["bones"]
    bone = next(b for b in bones if b["name"] == ("head" if worn else "floor"))
    return bone["cubes"], tex


SKIN = (196, 150, 120, 255)
SHIRT = (60, 160, 170, 255)
PLAYER = [
    ([{"origin": [-4, 24, -4], "size": [8, 8, 8]}], SKIN),
    ([{"origin": [-4, 12, -2], "size": [8, 12, 4]}], SHIRT),
    ([{"origin": [-8, 12, -2], "size": [4, 12, 4]}, {"origin": [4, 12, -2], "size": [4, 12, 4]}], SKIN),
]


def render(key, yaw=0, worn=False):
    cubes, tex = load(key, worn)
    size = (CELL_W, CELL_H - LABEL_H)
    if worn:
        parts = [(c, None, col) for c, col in PLAYER] + [(cubes, tex, None)]
        return draw_model(parts, size, yaw, scale=4.2 * CELL_W / 170)
    return draw_model([(cubes, tex, None)], size, yaw)


def label_font():
    try:
        return ImageFont.truetype("DejaVuSans.ttf", 12)
    except OSError:
        return ImageFont.load_default()


def sheet(heads, out, back=False, worn=False):
    views = [0, 180] if back else [0]
    per_row = min(len(heads), max(1, COLS // len(views)) if not worn else 6)
    cell_w = CELL_W * len(views)
    rows = math.ceil(len(heads) / per_row)
    img = Image.new("RGBA", (per_row * cell_w, max(1, rows) * CELL_H), (58, 52, 48, 255))
    draw = ImageDraw.Draw(img)
    font = label_font()
    for n, head in enumerate(heads):
        cx, cy = (n % per_row) * cell_w, (n // per_row) * CELL_H
        for v, yaw in enumerate(views):
            img.alpha_composite(render(head.key, yaw, worn), (cx + v * CELL_W, cy))
        label = head.name.replace(" Head", "").replace(" Skull", "")
        lines = [label]
        if draw.textlength(label, font=font) > cell_w - 8 and " " in label:
            words = label.split(" ")
            half = len(words) // 2
            lines = [" ".join(words[:half]), " ".join(words[half:])]
        for i, line in enumerate(lines):
            tw = draw.textlength(line, font=font)
            draw.text((cx + (cell_w - tw) / 2, cy + CELL_H - LABEL_H + i * 14), line,
                      fill=(240, 230, 210), font=font)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out)
    print(f"Wrote {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma separated mob key prefixes")
    ap.add_argument("--back", action="store_true", help="also show each head from behind")
    ap.add_argument("--worn", action="store_true", help="show heads worn by a player")
    ap.add_argument("--out", help="output PNG path")
    ap.add_argument("--zoom", type=float, default=1, help="cell size multiplier")
    args = ap.parse_args()
    global CELL_W, CELL_H
    CELL_W, CELL_H = int(CELL_W * args.zoom), int((CELL_H - LABEL_H) * args.zoom) + LABEL_H

    heads = [t for h in HEADS if not h.vanilla_item for t in trophies(h)]
    if args.only:
        prefixes = [p.strip() for p in args.only.split(",") if p.strip()]
        heads = [t for t in heads if any(t.key.startswith(p) or t.mob == p for p in prefixes)]
        if not heads:
            sys.exit("no heads match --only")
        sheet(heads, Path(args.out or "preview.png"), back=args.back, worn=args.worn)
        return

    if args.out:
        sheet(heads, Path(args.out), back=args.back, worn=args.worn)
        return
    sheet(heads, OUT, back=args.back)
    keys = {t.key: t for t in heads}
    showcase = [keys[k] for k in WORN_SHOWCASE if k in keys]
    sheet(showcase, WORN_OUT, back=True, worn=True)


if __name__ == "__main__":
    main()
