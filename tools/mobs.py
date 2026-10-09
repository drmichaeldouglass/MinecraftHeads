"""Mob head definitions for the Mob Trophies add-on.

Every mob gets one entry. Most entries describe a small voxel head model plus
pixel art, which build.py turns into a custom block, a wearable item, a
geometry file and a texture. Mobs that already have a vanilla head item
(creeper, zombie, ...) just point at that item instead.

The art itself lives in tools/art/, one file per group of mobs. This file
holds the data model, the helpers and the vanilla heads.

Coordinate system for a head (in pixels, 16 pixels = 1 block):
  * x runs from -W/2 to +W/2, y from 0 (bottom) to H, z from -D/2 to +D/2.
  * The face is the north side (z = -D/2). Snouts, beaks and noses therefore
    have negative z.
  * build.py moves the whole model into position for floor, wall and
    ceiling placement, and scales it to fit over a player's head when worn,
    so only describe it once here.

Pixel art strings are read top row first. Each character is a palette key;
"." is the mob's base colour (or the extra cube's own colour on extras).
How each face is drawn:
  * front (north):  as seen when looking at the face.
  * side (east and west):  as seen from the side, with the BACK of the head
    on the left and the face on the right. The same art is used on both
    sides (mirrored), unless `west` gives different art for the other side.
  * top (up):  as seen from above with the face at the BOTTOM of the grid.
  * back (south):  as seen from behind.
  * bottom (down):  as seen from below with the face at the TOP of the grid.
Art sizes: front/back are W x H, sides are D x H, top/bottom are W x D
(columns x rows).

Extra cubes take the same art through `faces`, a dict with any of the keys
"front", "back", "side", "west", "top" and "bottom" (or the raw face names
"north", "south", "east", "west", "up", "down"). `front=` still works as a
shortcut for the north face.

Variants: a mob whose look changes (cat breeds, sheep colours, villager
biomes, ...) lists them with V(...). Each variant becomes its own head with
its own block and item. The first variant is the default: it keeps the mob's
plain key (so heads from older versions of the add-on still work) and drops
when the game reports a variant we do not know about. Every other variant
gets the key "<mob>_<variant>".
"""

from dataclasses import dataclass, field, replace


@dataclass
class Cube:
    origin: tuple
    size: tuple
    letter: str = "."
    front: list = None
    faces: dict = field(default_factory=dict)


@dataclass
class Variant:
    key: str
    name: str
    match: dict
    changes: dict


@dataclass
class Head:
    key: str
    name: str
    category: str
    entities: list
    size: tuple = (8, 8, 8)
    pal: dict = field(default_factory=dict)
    front: list = None
    side: list = None
    west: list = None
    top: list = None
    back: list = None
    bottom: list = None
    top_fill: str = "."
    side_fill: str = "."
    back_fill: str = "."
    bottom_fill: str = "."
    extras: list = field(default_factory=list)
    vanilla_item: str = None
    experimental: bool = False
    variants: list = field(default_factory=list)
    # Worn on a player's head the model is scaled up to cover it. Set this to
    # force a different scale (1.0 = same size as the placed block).
    wear_scale: float = None
    # Filled in by trophies(): the mob this head belongs to and how the game
    # tells this variant apart (see V()).
    mob: str = None
    match: dict = None


def V(key, name, match=None, **changes):
    """A variant of a mob head.

    key:    short id, e.g. "tuxedo". The head key becomes "<mob>_<key>"
            (except for the first, default variant, which keeps "<mob>").
    name:   item name, e.g. "Tuxedo Cat Head".
    match:  what the game reports for this variant on the living mob. All
            entries must match. Supported keys:
              "variant":       the minecraft:variant component value
              "mark_variant":  the minecraft:mark_variant component value
              "color":         the minecraft:color component value (sheep)
              "skin_id":       the minecraft:skin_id component value
              any "namespace:name" key: an entity property, e.g.
              {"minecraft:climate_variant": "warm"}
    changes: any Head field to change for this variant (size, front, side,
            top, extras, ...). `pal` is merged into the mob's palette, so
            only list the colours that differ.
    """
    return Variant(key, name, match or {}, changes)


def trophies(head):
    """Expand a mob into the heads that can drop: one per variant."""
    if not head.variants:
        return [replace(head, mob=head.key, match={}, variants=[])]
    out = []
    for i, v in enumerate(head.variants):
        changes = dict(v.changes)
        pal = {**head.pal, **changes.pop("pal", {})}
        key = head.key if i == 0 else f"{head.key}_{v.key}"
        out.append(replace(head, key=key, name=v.name, pal=pal, mob=head.key,
                           match=dict(v.match), variants=[], **changes))
    return out


def mirror(art):
    return [row[::-1] for row in art] if art else art


def pair(x, y, z, size, letter=".", front=None, faces=None):
    """Two mirrored cubes (ears, horns, eyes). x is the left cube's min x.

    The second cube gets the art flipped left to right, so the pair is
    symmetric (an eye with its pupil on the inside stays on the inside).
    """
    w = size[0]
    faces = dict(faces or {})
    other = {k: mirror(v) if k in ("front", "north", "back", "south", "top", "up",
                                   "bottom", "down") else v
             for k, v in faces.items()}
    return [Cube((x, y, z), size, letter, front, faces),
            Cube((-x - w, y, z), size, letter, mirror(front), other)]


def snout(head_size, size, y, letter=".", front=None, faces=None):
    """A cube stuck to the middle of the face."""
    w, h, d = size
    return Cube((-w / 2, y, -head_size[2] / 2 - d), size, letter, front, dict(faces or {}))


def solid(w, h, ch="."):
    """A w x h block of one colour, handy as a starting point for art."""
    return [ch * w for _ in range(h)]


HEADS = []


def add(key, name, category, entities=None, **kw):
    HEADS.append(Head(key, name, category, entities or ["minecraft:" + key], **kw))


def vanilla(key, name, category, item):
    HEADS.append(Head(key, name, category, ["minecraft:" + key], vanilla_item=item))


K = "#151515"  # near black used for most eyes
W = "#f4f4f4"

# --------------------------------------------------------------------------
# Vanilla heads (the game already has these blocks/items)
# --------------------------------------------------------------------------
vanilla("creeper", "Creeper Head", "Hostile", "minecraft:creeper_head")
vanilla("zombie", "Zombie Head", "Hostile", "minecraft:zombie_head")
vanilla("skeleton", "Skeleton Skull", "Hostile", "minecraft:skeleton_skull")
vanilla("wither_skeleton", "Wither Skeleton Skull", "Hostile", "minecraft:wither_skeleton_skull")
vanilla("piglin", "Piglin Head", "Neutral", "minecraft:piglin_head")
vanilla("ender_dragon", "Dragon Head", "Boss", "minecraft:dragon_head")

# --------------------------------------------------------------------------
# Custom heads. Each module calls add() for its mobs, in ledger order.
# --------------------------------------------------------------------------
from art import passive_1, passive_2, neutral, hostile_1, hostile_2  # noqa: E402,F401
