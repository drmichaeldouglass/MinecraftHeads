#!/usr/bin/env python3
"""Generate the Mob Trophies behavior pack, resource pack and .mcaddon.

Usage:  python3 tools/build.py

Reads the head definitions in tools/mobs.py and writes:
  dist/MobTrophies_BP/      blocks, items, recipes, scripts, manifest
  dist/MobTrophies_RP/      geometry, textures, lang, manifest
  dist/MobTrophies.mcaddon  both packs zipped, ready to install

dist/ is wiped and rebuilt every time. Hand written scripts live in
src/scripts/ and are copied in; edit mobs.py rather than the generated JSON.
"""

import json
import random
import shutil
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from mobs import HEADS, Cube  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BP = DIST / "MobTrophies_BP"
RP = DIST / "MobTrophies_RP"
SCRIPTS_SRC = ROOT / "src" / "scripts"

NS = "mh"
VERSION = [1, 0, 0]
MIN_ENGINE = [1, 21, 90]
BLOCK_FORMAT = "1.21.90"
UUIDS = {
    "bp_header": "bb81b9f7-f058-4f54-9f28-a4475b4b1934",
    "bp_data": "71783bba-20d7-407b-951d-9e3d25f5d29e",
    "bp_script": "f12c436d-3e89-409f-9000-750a6b28b6f9",
    "rp_header": "5aea012c-1b44-4dd2-b3d9-a4e202fdcc3d",
    "rp_resources": "882411ec-0cc0-46d1-ae81-cfbb36d2c7e6",
}
SCRIPT_DEPS = [("@minecraft/server", "2.0.0"), ("@minecraft/server-ui", "2.0.0")]

DIRECTIONS = {"north": 0, "south": 180, "west": 90, "east": -90}
TEX_SIZE = 64


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def block_id(head):
    return f"{NS}:{head.key}_head"


def tex_name(head):
    return f"{NS}_{head.key}_head"


def cubes_of(head):
    """Head cube first, then extras. All in head-local coordinates."""
    w, h, d = head.size
    main = Cube((-w / 2, 0, -d / 2), head.size, ".", head.front)
    return [main] + list(head.extras)


def validate(head):
    w, h, d = head.size
    pal = head.pal
    if "." not in pal:
        raise ValueError(f"{head.key}: palette needs a '.' base colour")

    def check_art(art, aw, ah, what):
        if art is None:
            return
        if len(art) != ah or any(len(r) != aw for r in art):
            raise ValueError(f"{head.key}: {what} art must be {aw}x{ah}")
        for row in art:
            for ch in row:
                if ch not in pal:
                    raise ValueError(f"{head.key}: {what} uses unknown colour '{ch}'")

    check_art(head.front, w, h, "front")
    check_art(head.side, d, h, "side")
    for c in head.extras:
        if c.letter not in pal:
            raise ValueError(f"{head.key}: extra uses unknown colour '{c.letter}'")
        if any(int(s) != s or s <= 0 for s in c.size):
            raise ValueError(f"{head.key}: extra sizes must be positive whole numbers")
        check_art(c.front, c.size[0], c.size[1], "extra front")
    for f in (head.top_fill, head.side_fill, head.back_fill, head.bottom_fill):
        if f not in pal:
            raise ValueError(f"{head.key}: fill colour '{f}' not in palette")


# --------------------------------------------------------------------------
# Placement: floor, ceiling and wall variants of the same model
# --------------------------------------------------------------------------
def bounds(cubes):
    lo = [min(c.origin[i] for c in cubes) for i in range(3)]
    hi = [max(c.origin[i] + c.size[i] for c in cubes) for i in range(3)]
    return lo, hi


def placements(head):
    """Return {bone: (dx, dy, dz)} offsets and {bone: (origin, size)} boxes.

    All variants face north; the block's transformation component rotates
    them (and their collision boxes) to the right direction.
    """
    w, h, d = head.size
    cubes = cubes_of(head)
    lo, hi = bounds(cubes)
    if lo[1] < 0:
        raise ValueError(f"{head.key}: model goes below y=0")
    if hi[1] > 16:
        raise ValueError(f"{head.key}: model is taller than a block")

    wall_dy = min((16 - h) / 2, 16 - hi[1])
    offsets = {
        "floor": (0, 0, 0),
        "ceiling": (0, 16 - hi[1], 0),
        "wall": (0, wall_dy, 8 - d / 2),
    }
    boxes = {}
    for bone, (dx, dy, dz) in offsets.items():
        for c in cubes:
            for i, off in enumerate((dx, dy, dz)):
                a = c.origin[i] + off
                b = a + c.size[i]
                limit = (-8, 8) if i != 1 else (0, 16)
                if a < limit[0] or b > limit[1]:
                    raise ValueError(f"{head.key}: {bone} variant sticks out of the block "
                                     f"(axis {'xyz'[i]}: {a}..{b})")
        boxes[bone] = ([-w / 2 + dx, dy, -d / 2 + dz], [w, h, d])
    return offsets, boxes


# --------------------------------------------------------------------------
# Texture packing and painting
# --------------------------------------------------------------------------
def pack(cubes):
    """Shelf-pack box-UV regions. Returns list of (u, v)."""
    out = []
    x = y = shelf = 0
    for c in cubes:
        w, h, d = (int(s) for s in c.size)
        rw, rh = 2 * (w + d), d + h
        if x + rw > TEX_SIZE:
            x, y, shelf = 0, y + shelf, 0
        if rw > TEX_SIZE or y + rh > TEX_SIZE:
            raise ValueError("texture regions do not fit in the texture")
        out.append((x, y))
        x += rw
        shelf = max(shelf, rh)
    return out


def face_regions(u, v, w, h, d):
    return {
        "up": (u + d, v, w, d),
        "down": (u + d + w, v, w, d),
        "east": (u, v + d, d, h),
        "north": (u + d, v + d, w, h),
        "west": (u + d + w, v + d, d, h),
        "south": (u + 2 * d + w, v + d, w, h),
    }


def paint(head, cubes, uvs):
    img = Image.new("RGBA", (TEX_SIZE, TEX_SIZE), (0, 0, 0, 0))
    px = img.load()
    rng = random.Random(head.key)
    pal = {k: hex_to_rgb(v) for k, v in head.pal.items()}

    def put(x, y, letter):
        r, g, b = pal[letter]
        f = 1 + rng.uniform(-0.07, 0.07)
        px[x, y] = (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)), 255)

    def fill(region, letter, art=None):
        rx, ry, rw, rh = region
        for j in range(rh):
            for i in range(rw):
                ch = art[j][i] if art else letter
                put(rx + i, ry + j, letter if ch == "." else ch)

    for idx, (c, (u, v)) in enumerate(zip(cubes, uvs)):
        w, h, d = (int(s) for s in c.size)
        faces = face_regions(u, v, w, h, d)
        if idx == 0:
            fill(faces["north"], ".", head.front)
            fill(faces["east"], head.side_fill, head.side)
            fill(faces["west"], head.side_fill, [r[::-1] for r in head.side] if head.side else None)
            fill(faces["up"], head.top_fill)
            fill(faces["down"], head.bottom_fill)
            fill(faces["south"], head.back_fill)
        else:
            for name, region in faces.items():
                fill(region, c.letter, c.front if name == "north" else None)
    return img


# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------
def geometry(head, cubes, uvs, offsets):
    bones = []
    for bone, (dx, dy, dz) in offsets.items():
        geo_cubes = []
        for c, (u, v) in zip(cubes, uvs):
            w, h, d = (int(s) for s in c.size)
            f = face_regions(u, v, w, h, d)

            def face(name, flip=False):
                fu, fv, fw, fh = f[name]
                if flip:
                    return {"uv": [fu, fv + fh], "uv_size": [fw, -fh]}
                return {"uv": [fu, fv], "uv_size": [fw, fh]}

            geo_cubes.append({
                "origin": [c.origin[0] + dx, c.origin[1] + dy, c.origin[2] + dz],
                "size": list(c.size),
                "uv": {
                    "north": face("north"),
                    "east": face("east"),
                    "south": face("south"),
                    "west": face("west"),
                    "up": face("up"),
                    "down": face("down", flip=True),
                },
            })
        bones.append({"name": bone, "pivot": [0, 0, 0], "cubes": geo_cubes})
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": f"geometry.{NS}.{head.key}_head",
                "texture_width": TEX_SIZE,
                "texture_height": TEX_SIZE,
                "visible_bounds_width": 2,
                "visible_bounds_height": 2.5,
                "visible_bounds_offset": [0, 0.75, 0],
            },
            "bones": bones,
        }],
    }


# --------------------------------------------------------------------------
# Block definition
# --------------------------------------------------------------------------
def block_json(head, boxes):
    geo_id = f"geometry.{NS}.{head.key}_head"
    material = {"*": {"texture": tex_name(head), "render_method": "alpha_test"}}

    def geo(visible):
        return {"identifier": geo_id,
                "bone_visibility": {b: b == visible for b in ("floor", "ceiling", "wall")}}

    def box(bone):
        origin, size = boxes[bone]
        return {"origin": origin, "size": size}

    def variant(bone):
        return {
            "minecraft:geometry": geo(bone),
            "minecraft:material_instances": material,
            "minecraft:collision_box": box(bone),
            "minecraft:selection_box": box(bone),
        }

    face = "q.block_state('minecraft:block_face')"
    card = "q.block_state('minecraft:cardinal_direction')"
    perms = []
    for direction, angle in DIRECTIONS.items():
        rot = {"minecraft:transformation": {"rotation": [0, angle, 0]}}
        # Standing on a block: turn to face the player who placed it.
        perms.append({"condition": f"{face} == 'up' && {card} == '{direction}'",
                      "components": dict(rot)})
        # Hanging under a block.
        perms.append({"condition": f"{face} == 'down' && {card} == '{direction}'",
                      "components": {**variant("ceiling"), **rot}})
        # Mounted on the side of a block, facing away from it.
        perms.append({"condition": f"{face} == '{direction}'",
                      "components": {**variant("wall"), **rot}})

    base = hex_to_rgb(head.pal["."])
    return {
        "format_version": BLOCK_FORMAT,
        "minecraft:block": {
            "description": {
                "identifier": block_id(head),
                "menu_category": {"category": "items"},
                "traits": {
                    "minecraft:placement_position": {"enabled_states": ["minecraft:block_face"]},
                    "minecraft:placement_direction": {
                        "enabled_states": ["minecraft:cardinal_direction"],
                        "y_rotation_offset": 180,
                    },
                },
            },
            "components": {
                **variant("floor"),
                "minecraft:destructible_by_mining": {"seconds_to_destroy": 1},
                "minecraft:destructible_by_explosion": {"explosion_resistance": 1},
                "minecraft:light_dampening": 0,
                "minecraft:map_color": "#%02x%02x%02x" % base,
                "tag:mh_trophy": {},
            },
            "permutations": perms,
        },
    }


# --------------------------------------------------------------------------
# Trophy Ledger item + misc art
# --------------------------------------------------------------------------
LEDGER_ICON = [
    "................",
    "..bbbbbbbbbbb...",
    "..bgggggggggbp..",
    "..bgbbbbbbbgbp..",
    "..bgb.....bgbp..",
    "..bgb.y.y.bgbp..",
    "..bgb.yyy.bgbp..",
    "..bgb..y..bgbp..",
    "..bgb.....bgbp..",
    "..bgbbbbbbbgbp..",
    "..bgggggggggbp..",
    "..bgggggggggbp..",
    "..bgggggggggbp..",
    "..bbbbbbbbbbbp..",
    "...ppppppppppp..",
    "................",
]
LEDGER_PAL = {"b": "#4a2a14", "g": "#8b4d22", "y": "#f2c94c", "p": "#efe6d2"}


def ledger_icon():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(LEDGER_ICON):
        for x, ch in enumerate(row):
            if ch != ".":
                img.putpixel((x, y), hex_to_rgb(LEDGER_PAL[ch]) + (255,))
    return img


def pack_icon(textures):
    """A 4x4 grid of mob faces on a dark background."""
    img = Image.new("RGBA", (256, 256), (40, 32, 28, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 255, 255], outline=(214, 170, 72, 255), width=8)
    picks = ["cow", "pig", "enderman", "blaze", "sheep", "wolf", "fox", "slime",
             "villager", "spider", "warden", "panda", "witch", "axolotl", "frog", "bee"]
    for i, key in enumerate(picks):
        head, face = textures[key]
        tile = face.resize((48, int(48 * face.height / face.width)), Image.NEAREST)
        cx, cy = 16 + (i % 4) * 58 + 24, 16 + (i // 4) * 58 + 24
        img.alpha_composite(tile, (cx - tile.width // 2, cy - tile.height // 2))
    return img


def front_face(head, img, uvs):
    w, h, d = (int(s) for s in head.size)
    u, v = uvs[0]
    fx, fy, fw, fh = face_regions(u, v, w, h, d)["north"]
    return img.crop((fx, fy, fx + fw, fy + fh))


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def manifests():
    deps = [{"module_name": n, "version": v} for n, v in SCRIPT_DEPS]
    write_json(BP / "manifest.json", {
        "format_version": 2,
        "header": {
            "name": "pack.name",
            "description": "pack.description",
            "uuid": UUIDS["bp_header"],
            "version": VERSION,
            "min_engine_version": MIN_ENGINE,
        },
        "modules": [
            {"type": "data", "uuid": UUIDS["bp_data"], "version": VERSION},
            {"type": "script", "language": "javascript", "uuid": UUIDS["bp_script"],
             "version": VERSION, "entry": "scripts/main.js"},
        ],
        "dependencies": [{"uuid": UUIDS["rp_header"], "version": VERSION}] + deps,
        "metadata": {"authors": ["Michael Douglass"]},
    })
    write_json(RP / "manifest.json", {
        "format_version": 2,
        "header": {
            "name": "pack.name",
            "description": "pack.description",
            "uuid": UUIDS["rp_header"],
            "version": VERSION,
            "min_engine_version": MIN_ENGINE,
        },
        "modules": [{"type": "resources", "uuid": UUIDS["rp_resources"], "version": VERSION}],
        "dependencies": [{"uuid": UUIDS["bp_header"], "version": VERSION}],
        "metadata": {"authors": ["Michael Douglass"]},
    })


def clean():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()


def heads_js():
    entries = []
    for h in HEADS:
        entries.append({
            "key": h.key,
            "name": h.name,
            "category": h.category,
            "item": h.vanilla_item or block_id(h),
            "entities": h.entities,
            "experimental": h.experimental,
        })
    body = json.dumps(entries, indent=2)
    return ("// Generated by tools/build.py from tools/mobs.py. Do not edit by hand.\n"
            f"export const HEADS = {body};\n")


def lang(pack_desc):
    lines = ["pack.name=Mob Trophies", f"pack.description={pack_desc}"]
    return "\n".join(lines) + "\n"


def make_mcaddon():
    out = DIST / "MobTrophies.mcaddon"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for pack_dir in (BP, RP):
            for f in sorted(pack_dir.rglob("*")):
                if f.is_file():
                    # Fixed timestamp so rebuilding unchanged packs gives an identical file.
                    info = zipfile.ZipInfo(str(Path(pack_dir.name) / f.relative_to(pack_dir)),
                                           date_time=(2024, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    z.writestr(info, f.read_bytes())
    return out


def main():
    keys = [h.key for h in HEADS]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate head keys")
    seen = set()
    for h in HEADS:
        for e in h.entities:
            if e in seen:
                raise ValueError(f"{e} is mapped to more than one head")
            seen.add(e)

    clean()
    terrain = {}
    rp_lang = []
    textures = {}
    custom = [h for h in HEADS if not h.vanilla_item]
    for head in custom:
        validate(head)
        cubes = cubes_of(head)
        offsets, boxes = placements(head)
        uvs = pack(cubes)
        img = paint(head, cubes, uvs)
        tex_dir = RP / "textures" / "blocks" / "heads"
        tex_dir.mkdir(parents=True, exist_ok=True)
        img.save(tex_dir / f"{head.key}_head.png")
        textures[head.key] = (head, front_face(head, img, uvs))
        write_json(RP / "models" / "blocks" / "heads" / f"{head.key}_head.geo.json",
                   geometry(head, cubes, uvs, offsets))
        write_json(BP / "blocks" / "heads" / f"{head.key}_head.json", block_json(head, boxes))
        terrain[tex_name(head)] = {"textures": f"textures/blocks/heads/{head.key}_head"}
        rp_lang.append(f"tile.{block_id(head)}.name={head.name}")

    # Resource pack
    write_json(RP / "textures" / "terrain_texture.json", {
        "resource_pack_name": "mob_trophies",
        "texture_name": "atlas.terrain",
        "padding": 8,
        "num_mip_levels": 4,
        "texture_data": terrain,
    })
    write_json(RP / "blocks.json", {
        "format_version": [1, 1, 0],
        **{block_id(h): {"sound": "stone"} for h in custom},
    })
    write_json(RP / "textures" / "item_texture.json", {
        "resource_pack_name": "mob_trophies",
        "texture_name": "atlas.items",
        "texture_data": {"mh_trophy_ledger": {"textures": "textures/items/trophy_ledger"}},
    })
    (RP / "textures" / "items").mkdir(parents=True, exist_ok=True)
    ledger_icon().save(RP / "textures" / "items" / "trophy_ledger.png")

    rp_desc = "Mob head trophies: textures and models"
    bp_desc = "Every mob drops its head when a player kills it. Collect them all!"
    (RP / "texts").mkdir(parents=True, exist_ok=True)
    (RP / "texts" / "en_US.lang").write_text(
        lang(rp_desc) + "\n".join(rp_lang) + "\n")
    write_json(RP / "texts" / "languages.json", ["en_US"])
    (BP / "texts").mkdir(parents=True, exist_ok=True)
    (BP / "texts" / "en_US.lang").write_text(lang(bp_desc))
    write_json(BP / "texts" / "languages.json", ["en_US"])

    # Behavior pack items, recipes and script data
    write_json(BP / "items" / "trophy_ledger.json", {
        "format_version": BLOCK_FORMAT,
        "minecraft:item": {
            "description": {
                "identifier": "mh:trophy_ledger",
                "menu_category": {"category": "equipment"},
            },
            "components": {
                "minecraft:icon": {"textures": {"default": "mh_trophy_ledger"}},
                "minecraft:display_name": {"value": "Trophy Ledger"},
                "minecraft:max_stack_size": 1,
                "minecraft:glint": True,
            },
        },
    })
    write_json(BP / "recipes" / "trophy_ledger.json", {
        "format_version": "1.20.10",
        "minecraft:recipe_shapeless": {
            "description": {"identifier": "mh:trophy_ledger"},
            "tags": ["crafting_table"],
            "unlock": [{"item": "minecraft:book"}],
            "ingredients": [{"item": "minecraft:book"}, {"item": "minecraft:bone"}],
            "result": {"item": "mh:trophy_ledger"},
        },
    })
    shutil.copytree(SCRIPTS_SRC, BP / "scripts")
    (BP / "scripts" / "heads.js").write_text(heads_js())

    manifests()
    icon = pack_icon(textures)
    icon.save(BP / "pack_icon.png")
    icon.save(RP / "pack_icon.png")

    out = make_mcaddon()
    required = sum(1 for h in HEADS if not h.experimental)
    print(f"Built {len(custom)} custom heads + {len(HEADS) - len(custom)} vanilla heads "
          f"({required} required for the collection). Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
