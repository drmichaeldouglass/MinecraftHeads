#!/usr/bin/env python3
"""Generate the Mob Trophies behavior pack, resource pack and .mcaddon.

Usage:  python3 tools/build.py

Reads the head definitions in tools/mobs.py (art in tools/art/) and writes:
  dist/MobTrophies_BP/      blocks, items, recipes, scripts, manifest
  dist/MobTrophies_RP/      geometry, attachables, textures, lang, manifest
  dist/MobTrophies.mcaddon  both packs zipped, ready to install

dist/ is wiped and rebuilt every time. Hand written scripts live in
src/scripts/ and are copied in; edit mobs.py rather than the generated JSON.

Every custom head is a block (placed on the floor, a wall or a ceiling) whose
item is replaced by a wearable item, so heads can go in the helmet slot. An
attachable draws the head scaled up over the wearer's own head.
"""

import json
import random
import shutil
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from mobs import HEADS, Cube, trophies  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BP = DIST / "MobTrophies_BP"
RP = DIST / "MobTrophies_RP"
SCRIPTS_SRC = ROOT / "src" / "scripts"

NS = "mh"
VERSION = [1, 2, 0]
MIN_ENGINE = [1, 21, 90]
BLOCK_FORMAT = "1.21.90"
ITEM_FORMAT = "1.21.90"
UUIDS = {
    "bp_header": "bb81b9f7-f058-4f54-9f28-a4475b4b1934",
    "bp_data": "71783bba-20d7-407b-951d-9e3d25f5d29e",
    "bp_script": "f12c436d-3e89-409f-9000-750a6b28b6f9",
    "rp_header": "5aea012c-1b44-4dd2-b3d9-a4e202fdcc3d",
    "rp_resources": "882411ec-0cc0-46d1-ae81-cfbb36d2c7e6",
}
SCRIPT_DEPS = [("@minecraft/server", "2.0.0"), ("@minecraft/server-ui", "2.0.0")]

DIRECTIONS = {"north": 0, "south": 180, "west": 90, "east": -90}
TEX_SIZES = (64, 128)
FACES = ("north", "east", "south", "west", "up", "down")
ART_KEYS = {"front": "north", "back": "south", "side": "east", "top": "up", "bottom": "down"}

# Worn heads are scaled so they cover the player's 8x8x8 head with a little
# room to spare, like the vanilla skulls do.
WEAR_COVER = 9.0
WEAR_MIN_SCALE = 1.0
WEAR_MAX_SCALE = 2.25
PLAYER_HEAD_PIVOT = [0, 24, 0]
PLAYER_HEAD_BOTTOM = 23.5
PLAYER_HEAD_TOP = 32.5


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


def mirror(art):
    return [row[::-1] for row in art] if art else art


def cube_art(cube):
    """{face: (art or None, fill letter)} for an extra cube."""
    faces = {}
    for k, art in (cube.faces or {}).items():
        faces[ART_KEYS.get(k, k)] = art
    if cube.front is not None:
        faces.setdefault("north", cube.front)
    if "east" in faces and "west" not in faces:
        faces["west"] = faces["east"]
    out = {}
    for f in FACES:
        art = faces.get(f)
        # Side art is drawn with the back on the left; the west face shows it
        # from the other side, so flip it to keep the face end at the front.
        out[f] = (mirror(art) if f == "west" else art, cube.letter)
    return out


def main_cube(head):
    w, h, d = head.size
    side = head.side
    west = head.west if head.west is not None else side
    faces = {
        "north": (head.front, "."),
        "east": (side, head.side_fill),
        "west": (mirror(west), head.side_fill),
        "up": (head.top, head.top_fill),
        "down": (head.bottom, head.bottom_fill),
        "south": (head.back, head.back_fill),
    }
    return Cube((-w / 2, 0, -d / 2), head.size, ".", None, {"_resolved": faces})


def cubes_of(head):
    """Head cube first, then extras. All in head-local coordinates."""
    return [main_cube(head)] + list(head.extras)


def resolved_art(cube):
    if "_resolved" in (cube.faces or {}):
        return cube.faces["_resolved"]
    return cube_art(cube)


def art_size(face, size):
    w, h, d = (int(s) for s in size)
    return {"north": (w, h), "south": (w, h), "east": (d, h), "west": (d, h),
            "up": (w, d), "down": (w, d)}[face]


def validate(head):
    pal = head.pal
    if "." not in pal:
        raise ValueError(f"{head.key}: palette needs a '.' base colour")
    for k, v in pal.items():
        if len(k) != 1:
            raise ValueError(f"{head.key}: palette keys must be single characters, not {k!r}")
        try:
            hex_to_rgb(v)
        except ValueError:
            raise ValueError(f"{head.key}: palette colour {k!r} is not a #rrggbb value") from None
    if any(int(s) != s or s <= 0 for s in head.size):
        raise ValueError(f"{head.key}: head size must be positive whole numbers")

    for n, c in enumerate(cubes_of(head)):
        what = "head" if n == 0 else f"extra #{n}"
        if c.letter not in pal:
            raise ValueError(f"{head.key}: {what} uses unknown colour '{c.letter}'")
        if any(int(s) != s or s <= 0 for s in c.size):
            raise ValueError(f"{head.key}: {what} sizes must be positive whole numbers")
        if n and set(c.faces or {}) - set(ART_KEYS) - set(FACES):
            raise ValueError(f"{head.key}: {what} has unknown face names "
                             f"{sorted(set(c.faces) - set(ART_KEYS) - set(FACES))}")
        for face, (art, fill) in resolved_art(c).items():
            if fill not in pal:
                raise ValueError(f"{head.key}: {what} {face} fill colour '{fill}' not in palette")
            if art is None:
                continue
            aw, ah = art_size(face, c.size)
            if len(art) != ah or any(len(r) != aw for r in art):
                raise ValueError(f"{head.key}: {what} {face} art must be {aw} wide x {ah} tall")
            for row in art:
                for ch in row:
                    if ch not in pal:
                        raise ValueError(f"{head.key}: {what} {face} art uses unknown colour '{ch}'")


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
        # Push the model back until its rearmost part touches the wall.
        "wall": (0, wall_dy, 8 - hi[2]),
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
def pack(cubes, size):
    """Shelf-pack box-UV regions. Returns list of (u, v), or None if full."""
    out = []
    x = y = shelf = 0
    for c in cubes:
        w, h, d = (int(s) for s in c.size)
        rw, rh = 2 * (w + d), d + h
        if x + rw > size:
            x, y, shelf = 0, y + shelf, 0
        if rw > size or y + rh > size:
            return None
        out.append((x, y))
        x += rw
        shelf = max(shelf, rh)
    return out


def layout(head):
    cubes = cubes_of(head)
    # Biggest cubes first packs tighter; remember the original order.
    order = sorted(range(len(cubes)), key=lambda i: -(cubes[i].size[0] + cubes[i].size[2]))
    for size in TEX_SIZES:
        packed = pack([cubes[i] for i in order], size)
        if packed:
            uvs = [None] * len(cubes)
            for i, uv in zip(order, packed):
                uvs[i] = uv
            return cubes, uvs, size
    raise ValueError(f"{head.key}: texture regions do not fit in a {TEX_SIZES[-1]}px texture")


def face_regions(u, v, w, h, d):
    return {
        "up": (u + d, v, w, d),
        "down": (u + d + w, v, w, d),
        "east": (u, v + d, d, h),
        "north": (u + d, v + d, w, h),
        "west": (u + d + w, v + d, d, h),
        "south": (u + 2 * d + w, v + d, w, h),
    }


def paint(head, cubes, uvs, size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    rng = random.Random(head.key)
    pal = {k: hex_to_rgb(v) for k, v in head.pal.items()}

    def put(x, y, letter):
        r, g, b = pal[letter]
        f = 1 + rng.uniform(-0.06, 0.06)
        px[x, y] = (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)), 255)

    for c, (u, v) in zip(cubes, uvs):
        w, h, d = (int(s) for s in c.size)
        regions = face_regions(u, v, w, h, d)
        for face, (art, fill) in resolved_art(c).items():
            rx, ry, rw, rh = regions[face]
            for j in range(rh):
                for i in range(rw):
                    ch = art[j][i] if art else fill
                    put(rx + i, ry + j, fill if ch == "." else ch)
    return img


# --------------------------------------------------------------------------
# Geometry
# --------------------------------------------------------------------------
def geo_cube(c, uv, offset=(0, 0, 0), scale=(1, 1, 1)):
    u, v = uv
    w, h, d = (int(s) for s in c.size)
    f = face_regions(u, v, w, h, d)

    def face(name, flip=False):
        fu, fv, fw, fh = f[name]
        if flip:
            return {"uv": [fu, fv + fh], "uv_size": [fw, -fh]}
        return {"uv": [fu, fv], "uv_size": [fw, fh]}

    return {
        "origin": [round(c.origin[i] * scale[i] + offset[i], 4) for i in range(3)],
        "size": [round(c.size[i] * scale[i], 4) for i in range(3)],
        "uv": {
            "north": face("north"),
            "east": face("east"),
            "south": face("south"),
            "west": face("west"),
            "up": face("up"),
            "down": face("down", flip=True),
        },
    }


def geometry(head, cubes, uvs, offsets, size):
    bones = []
    for bone, off in offsets.items():
        bones.append({"name": bone, "pivot": [0, 0, 0],
                      "cubes": [geo_cube(c, uv, off) for c, uv in zip(cubes, uvs)]})
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": f"geometry.{NS}.{head.key}_head",
                "texture_width": size,
                "texture_height": size,
                "visible_bounds_width": 2,
                "visible_bounds_height": 2.5,
                "visible_bounds_offset": [0, 0.75, 0],
            },
            "bones": bones,
        }],
    }


def wear_transform(head):
    """Scale (x, y, z) and offset that sit the head over a player's head."""
    w, h, d = head.size
    s = head.wear_scale or min(WEAR_MAX_SCALE, max(WEAR_MIN_SCALE, WEAR_COVER / min(w, d)))
    sx, sy, sz = max(s, WEAR_COVER / w), s, max(s, WEAR_COVER / d)
    # Cover the top of the player's head; short heads sit on it like a hat.
    base = max(PLAYER_HEAD_BOTTOM, PLAYER_HEAD_TOP - h * sy)
    return (sx, sy, sz), (0, base, 0)


def worn_geometry(head, cubes, uvs, size):
    scale, offset = wear_transform(head)
    lo, hi = bounds(cubes)
    top = hi[1] * scale[1] + offset[1]
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": f"geometry.{NS}.{head.key}_head.worn",
                "texture_width": size,
                "texture_height": size,
                "visible_bounds_width": 3,
                "visible_bounds_height": max(3, top / 16 + 1),
                "visible_bounds_offset": [0, 1.5, 0],
            },
            # Same skeleton as the vanilla helmet model, so the head follows
            # the wearer's head as it turns and nods.
            "bones": [
                {"name": "waist", "pivot": [0, 12, 0]},
                {"name": "body", "parent": "waist", "pivot": [0, 24, 0]},
                {"name": "head", "parent": "body", "pivot": PLAYER_HEAD_PIVOT,
                 "cubes": [geo_cube(c, uv, offset, scale) for c, uv in zip(cubes, uvs)]},
            ],
        }],
    }


def attachable(head):
    item = block_id(head)
    return {
        "format_version": "1.10.0",
        "minecraft:attachable": {
            "description": {
                "identifier": item,
                # Only take over rendering while worn; held in a hand the item
                # keeps its normal block look.
                "item": {item: f"query.is_item_name_any('slot.armor.head', 0, '{item}')"},
                "materials": {"default": "entity_alphatest", "enchanted": "entity_alphatest_glint"},
                "textures": {
                    "default": f"textures/blocks/heads/{head.key}_head",
                    "enchanted": "textures/misc/enchanted_item_glint",
                },
                "geometry": {"default": f"geometry.{NS}.{head.key}_head.worn"},
                "scripts": {"parent_setup": "variable.helmet_layer_visible = 0.0;"},
                "render_controllers": ["controller.render.item_default"],
            },
        },
    }


# --------------------------------------------------------------------------
# Block and item definitions
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
            # No menu_category: the wearable item below stands in for the block.
            "description": {
                "identifier": block_id(head),
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


def item_json(head):
    """Replaces the block's own item so the head can also be worn."""
    return {
        "format_version": ITEM_FORMAT,
        "minecraft:item": {
            "description": {
                "identifier": block_id(head),
                "menu_category": {"category": "items", "group": "minecraft:itemGroup.name.skull"},
            },
            "components": {
                "minecraft:block_placer": {"block": block_id(head), "replace_block_item": True},
                "minecraft:display_name": {"value": f"tile.{block_id(head)}.name"},
                "minecraft:wearable": {"slot": "slot.armor.head", "protection": 0},
                "minecraft:max_stack_size": 64,
                "minecraft:rarity": "uncommon",
            },
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


def pack_icon(faces):
    """A 4x4 grid of mob faces on a dark background."""
    img = Image.new("RGBA", (256, 256), (40, 32, 28, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 255, 255], outline=(214, 170, 72, 255), width=8)
    picks = ["cow", "pig", "enderman", "blaze", "sheep", "wolf", "fox", "slime",
             "villager", "spider", "warden", "panda", "witch", "axolotl", "frog", "bee"]
    for i, key in enumerate(picks):
        face = faces[key]
        scale = 48 / max(face.width, face.height)
        tile = face.resize((max(1, round(face.width * scale)), max(1, round(face.height * scale))),
                           Image.NEAREST)
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


def mob_name(head):
    for suffix in (" Head", " Skull"):
        if head.name.endswith(suffix):
            return head.name[: -len(suffix)]
    return head.name


def heads_js():
    mobs = []
    for h in HEADS:
        mobs.append({
            "key": h.key,
            "name": mob_name(h),
            "category": h.category,
            "entities": h.entities,
            "experimental": h.experimental,
            "heads": [{"key": t.key, "name": t.name, "item": t.vanilla_item or block_id(t),
                       "match": t.match} for t in trophies(h)],
        })
    body = json.dumps(mobs, indent=2)
    return ("// Generated by tools/build.py from tools/mobs.py. Do not edit by hand.\n"
            f"export const MOBS = {body};\n")


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


def check_keys():
    keys = [h.key for h in HEADS]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate mob keys")
    seen_entities = set()
    seen_heads = set()
    for h in HEADS:
        for e in h.entities:
            if e in seen_entities:
                raise ValueError(f"{e} is mapped to more than one head")
            seen_entities.add(e)
        variant_keys = [v.key for v in h.variants]
        if len(variant_keys) != len(set(variant_keys)):
            raise ValueError(f"{h.key}: duplicate variant keys")
        matches = [json.dumps(v.match, sort_keys=True) for v in h.variants]
        if len(matches) != len(set(matches)):
            raise ValueError(f"{h.key}: two variants have the same match")
        for t in trophies(h):
            if t.key in seen_heads:
                raise ValueError(f"head key {t.key} is used twice")
            seen_heads.add(t.key)


def main():
    check_keys()
    clean()
    terrain = {}
    rp_lang = []
    faces = {}
    custom = [t for h in HEADS if not h.vanilla_item for t in trophies(h)]
    tex_dir = RP / "textures" / "blocks" / "heads"
    tex_dir.mkdir(parents=True, exist_ok=True)
    for head in custom:
        validate(head)
        offsets, boxes = placements(head)
        cubes, uvs, size = layout(head)
        img = paint(head, cubes, uvs, size)
        img.save(tex_dir / f"{head.key}_head.png")
        faces[head.key] = front_face(head, img, uvs)
        write_json(RP / "models" / "blocks" / "heads" / f"{head.key}_head.geo.json",
                   geometry(head, cubes, uvs, offsets, size))
        write_json(RP / "models" / "entity" / "heads" / f"{head.key}_head.worn.geo.json",
                   worn_geometry(head, cubes, uvs, size))
        write_json(RP / "attachables" / "heads" / f"{head.key}_head.json", attachable(head))
        write_json(BP / "blocks" / "heads" / f"{head.key}_head.json", block_json(head, boxes))
        write_json(BP / "items" / "heads" / f"{head.key}_head.json", item_json(head))
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
    icon = pack_icon(faces)
    icon.save(BP / "pack_icon.png")
    icon.save(RP / "pack_icon.png")

    out = make_mcaddon()
    mobs = [h for h in HEADS if not h.vanilla_item]
    required = sum(1 for h in HEADS if not h.experimental)
    print(f"Built {len(custom)} custom heads for {len(mobs)} mobs (with variants) + "
          f"{len(HEADS) - len(mobs)} vanilla heads ({required} mobs required for the "
          f"collection). Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

