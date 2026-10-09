"""Mob head definitions for the Mob Trophies add-on.

Every mob gets one entry. Most entries describe a small voxel head model plus
pixel art, which build.py turns into a custom block, a geometry file and a
texture. Mobs that already have a vanilla head item (creeper, zombie, ...)
just point at that item instead.

Coordinate system for a head (in pixels, 16 pixels = 1 block):
  * x runs from -W/2 to +W/2, y from 0 (bottom) to H, z from -D/2 to +D/2.
  * The face is the north side (z = -D/2). Snouts, beaks and noses therefore
    have negative z.
  * build.py moves the whole model into position for floor, wall and
    ceiling placement, so only describe it once here.

Pixel art strings are read top row first. Each character is a palette key;
"." is the mob's base colour (or the extra cube's own colour on extras).
"""

from dataclasses import dataclass, field


@dataclass
class Cube:
    origin: tuple
    size: tuple
    letter: str = "."
    front: list = None


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
    top_fill: str = "."
    side_fill: str = "."
    back_fill: str = "."
    bottom_fill: str = "."
    extras: list = field(default_factory=list)
    vanilla_item: str = None
    experimental: bool = False


def pair(x, y, z, size, letter=".", front=None):
    """Two mirrored cubes (ears, horns, eyes). x is the left cube's min x."""
    w = size[0]
    return [Cube((x, y, z), size, letter, front), Cube((-x - w, y, z), size, letter, front)]


def snout(head_size, size, y, letter=".", front=None):
    """A cube stuck to the middle of the face."""
    w, h, d = size
    return Cube((-w / 2, y, -head_size[2] / 2 - d), size, letter, front)


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
# Passive mobs
# --------------------------------------------------------------------------
add("allay", "Allay Head", "Passive", size=(6, 6, 6),
    pal={".": "#62d5f7", "w": "#b9f1ff", "b": "#1d3c8f"},
    front=["wwwwww",
           "......",
           ".b..b.",
           ".b..b.",
           "......",
           "......"])

add("armadillo", "Armadillo Head", "Passive", size=(6, 6, 6),
    pal={".": "#b37e6e", "d": "#7e5248", "k": K, "p": "#d9a296"},
    front=["......",
           "......",
           "k....k",
           "......",
           "......",
           "dddddd"],
    extras=pair(-3, 6, 1, (2, 2, 1), "p") + [snout((6, 6, 6), (2, 2, 3), 0, "p")])

add("axolotl", "Axolotl Head", "Passive", size=(8, 5, 5),
    pal={".": "#f4a6c6", "d": "#d34f87", "k": "#2a1520", "m": "#c6668f"},
    front=["........",
           "k......k",
           "........",
           "..mmmm..",
           "........"],
    extras=[Cube((-4, 5, 0), (8, 3, 1), "d")] + pair(-7, 1, 0, (3, 5, 1), "d"))

add("bat", "Bat Head", "Passive", size=(6, 6, 6),
    pal={".": "#4b3a2c", "d": "#2e2219", "k": K, "w": "#e8e0d0"},
    front=["......",
           "......",
           "k....k",
           "......",
           ".w..w.",
           "......"],
    extras=pair(-3, 6, 0, (2, 3, 1), "d"))

add("camel", "Camel Head", "Passive", size=(6, 6, 6),
    pal={".": "#d4a76a", "d": "#a77c45", "k": "#2b1d10"},
    front=["......",
           "......",
           "k....k",
           "......",
           "......",
           "......"],
    extras=[snout((6, 6, 6), (4, 4, 4), 0, ".", ["....", "....", "d..d", "...."])]
    + pair(-3, 6, 1, (1, 2, 1), "d"))

add("cat", "Cat Head", "Passive", size=(6, 6, 6),
    pal={".": "#c08a4f", "d": "#8a5a2c", "g": "#5fae43", "k": K, "p": "#e3a0a0", "w": "#e8dccb"},
    front=["d.dd.d",
           "......",
           "gk..kg",
           "......",
           "..pp..",
           ".w..w."],
    extras=pair(-3, 6, 0, (2, 2, 1), "d"))

add("chicken", "Chicken Head", "Passive", size=(4, 6, 3),
    pal={".": W, "k": K, "y": "#e8a92b", "r": "#cc2a2a"},
    front=["....",
           "k..k",
           "....",
           "....",
           "....",
           "...."],
    extras=[snout((4, 6, 3), (4, 2, 2), 2, "y"), snout((4, 6, 3), (2, 2, 1), 0, "r")])

add("cod", "Cod Head", "Passive", size=(6, 6, 6),
    pal={".": "#b8a07a", "d": "#8b7656", "k": K, "w": "#e7dcc7"},
    front=["dddddd",
           "d....d",
           "wk..kw",
           "......",
           "..dd..",
           "wwwwww"],
    extras=[Cube((-0.5, 6, -1), (1, 2, 3), "d")])

add("copper_golem", "Copper Golem Head", "Passive", size=(8, 6, 6),
    pal={".": "#c46d4a", "d": "#8f4a2f", "l": "#e5946a", "k": "#1e2a33"},
    front=["llllllll",
           "........",
           ".kk..kk.",
           "........",
           "........",
           "dddddddd"],
    extras=[snout((8, 6, 6), (2, 3, 2), 1, "d"),
            Cube((-0.5, 6, -0.5), (1, 4, 1), "l"),
            Cube((-1, 10, -1), (2, 2, 2), "l")])

COW = ["........",
       "..wwww..",
       "...ww...",
       "kw.ww.wk",
       "...ww...",
       "........",
       "........",
       "........"]
add("cow", "Cow Head", "Passive", size=(8, 8, 6),
    pal={".": "#3e2c22", "w": "#e9e4dd", "k": K, "m": "#b3a8a0", "n": "#5a4d47", "h": "#d8d0c0"},
    front=COW,
    extras=[snout((8, 8, 6), (4, 3, 1), 0, "m", ["....", "n..n", "...."])]
    + pair(-5, 6, 0, (1, 3, 1), "h"))

add("donkey", "Donkey Head", "Passive", size=(6, 6, 6),
    pal={".": "#8a7a68", "d": "#5b4f43", "l": "#bcae9c", "k": K},
    front=["dddddd", "......", "k....k", "......", "......", "......"],
    extras=[snout((6, 6, 6), (4, 4, 5), 0, "l", ["....", "....", "d..d", "...."])]
    + pair(-3, 6, 1, (2, 5, 1), "."))

add("frog", "Frog Head", "Passive", size=(8, 4, 8),
    pal={".": "#d07446", "d": "#a2532c", "k": K, "l": "#efc79a"},
    front=["dddddddd", "........", "llllllll", "llllllll"],
    extras=pair(-4, 4, -4, (3, 2, 3), ".", ["...", ".k."]))

add("glow_squid", "Glow Squid Head", "Passive",
    pal={".": "#1f6f74", "c": "#7ff5e0", "d": "#14494c"},
    front=["dddddddd",
           "d......d",
           "........",
           ".cc..cc.",
           ".cc..cc.",
           "........",
           "c.c..c.c",
           "........"])

add("happy_ghast", "Happy Ghast Head", "Passive",
    pal={".": "#f4f4f4", "k": "#1a1a1a", "p": "#f2a5b8"},
    front=["........",
           "........",
           ".kk..kk.",
           ".kk..kk.",
           "p......p",
           "..k..k..",
           "...kk...",
           "........"])

add("horse", "Horse Head", "Passive", size=(6, 6, 6),
    pal={".": "#8b5a2f", "d": "#4f2e15", "l": "#7a4c25", "k": K},
    front=["dddddd", "......", "k....k", "......", "......", "......"],
    extras=[snout((6, 6, 6), (4, 4, 5), 0, "l", ["....", "....", "d..d", "...."]),
            Cube((-1, 6, -3), (2, 2, 6), "d")]
    + pair(-3, 6, 1, (1, 2, 1), "."))

add("mooshroom", "Mooshroom Head", "Passive", size=(8, 8, 6),
    pal={".": "#a3241f", "w": "#dcdcdc", "k": K, "m": "#b3a8a0", "n": "#5a4d47",
         "h": "#d8d0c0", "r": "#d33a2c"},
    front=["........",
           "..wwww..",
           "...ww...",
           "kw.ww.wk",
           "...ww...",
           "........",
           "w......w",
           "ww....ww"],
    extras=[snout((8, 8, 6), (4, 3, 1), 0, "m", ["....", "n..n", "...."]),
            Cube((-3, 8, -1), (1, 2, 1), "w"), Cube((-4, 10, -2), (3, 1, 3), "r"),
            Cube((2, 8, 0), (1, 2, 1), "w"), Cube((1, 10, -1), (3, 1, 3), "r")]
    + pair(-5, 6, 0, (1, 3, 1), "h"))

add("mule", "Mule Head", "Passive", size=(6, 6, 6),
    pal={".": "#6b4a33", "d": "#3e2a1c", "l": "#8a6a52", "k": K},
    front=["dddddd", "......", "k....k", "......", "......", "......"],
    extras=[snout((6, 6, 6), (4, 4, 5), 0, "l", ["....", "....", "d..d", "...."])]
    + pair(-3, 6, 1, (2, 4, 1), "."))

add("nautilus", "Nautilus Head", "Passive",
    pal={".": "#e9dfcf", "s": "#b5652e", "k": K, "t": "#c98d6a"},
    front=["s.s.s.s.",
           "........",
           "ss.ss.ss",
           "........",
           "k......k",
           "tttttttt",
           "t.tt.tt.",
           "t.t..t.t"],
    side=["s.s.s.s.", "........", "ss.ss.ss", "........",
          "s.s.s.s.", "........", "ss.ss.ss", "........"])

add("ocelot", "Ocelot Head", "Passive", size=(6, 6, 6),
    pal={".": "#e3bf55", "d": "#7b5b2a", "g": "#4fae46", "k": K, "p": "#d99a8f"},
    front=["d.dd.d", "......", "gk..kg", "......", "..pp..", ".d..d."],
    extras=pair(-3, 6, 0, (2, 2, 1), "."))

add("parrot", "Parrot Head", "Passive", size=(6, 6, 6),
    pal={".": "#d82a24", "y": "#f0d13a", "k": K, "b": "#3a3a3a"},
    front=["......", "......", "yk..ky", "yy..yy", "......", "......"],
    extras=[snout((6, 6, 6), (2, 3, 2), 1, "b"), Cube((-0.5, 6, -1), (1, 2, 2), ".")])

add("pig", "Pig Head", "Passive",
    pal={".": "#efa8a3", "d": "#c9706c", "k": K, "w": W, "n": "#f2b9b5"},
    front=["........",
           "........",
           "........",
           "........",
           "kw....wk",
           "........",
           "........",
           "........"],
    extras=[snout((8, 8, 8), (4, 3, 1), 1, "n", ["....", "d..d", "...."])])

add("rabbit", "Rabbit Head", "Passive", size=(6, 5, 5),
    pal={".": "#9a7553", "d": "#6e5139", "k": K, "p": "#f2a6b0", "w": "#e7dccb"},
    front=["......", "k....k", "......", "..pp..", ".w..w."],
    extras=pair(-3, 5, 0, (2, 5, 1), "d"))

add("salmon", "Salmon Head", "Passive", size=(6, 6, 6),
    pal={".": "#a8433a", "d": "#5e7360", "k": K, "w": "#e2d3c0"},
    front=["dddddd", "dd..dd", "wk..kw", "......", "......", "......"],
    top_fill="d",
    extras=[Cube((-0.5, 6, 0), (1, 2, 2), "d")])

add("sheep", "Sheep Head", "Passive",
    pal={".": "#d9b896", "w": "#ecebe6", "k": K, "p": "#c58f7a"},
    front=["wwwwwwww",
           "wwwwwwww",
           "w......w",
           "w.k..k.w",
           "w......w",
           "w..pp..w",
           "w......w",
           "ww....ww"],
    top_fill="w", side_fill="w", back_fill="w")

add("skeleton_horse", "Skeleton Horse Head", "Passive", size=(6, 6, 6),
    pal={".": "#d6d3c4", "d": "#a19e8e", "k": "#2a2a2a"},
    front=["dddddd", "......", "kk..kk", "kk..kk", "......", "......"],
    extras=[snout((6, 6, 6), (4, 4, 5), 0, ".", ["....", "....", "k..k", "d.d."])]
    + pair(-3, 6, 1, (1, 2, 1), "d"))

add("sniffer", "Sniffer Head", "Passive",
    pal={".": "#a33d2e", "d": "#6e231a", "g": "#5ba34a", "k": K, "n": "#c25a3c"},
    front=["gggggggg",
           "g.gg.g.g",
           "........",
           "k......k",
           "........",
           "........",
           "........",
           "........"],
    top_fill="g",
    extras=[snout((8, 8, 8), (4, 3, 4), 1, "n", ["....", "d..d", "...."])])

add("snow_golem", "Snow Golem Head", "Passive",
    pal={".": "#e38a1d", "d": "#b8650f", "k": "#3a2005", "g": "#4e6b1f"},
    front=["........",
           "........",
           ".kk..kk.",
           ".kk..kk.",
           "........",
           ".kkkkkk.",
           "..k..k..",
           "........"],
    side=["..d...d."] * 8,
    extras=[Cube((-1, 8, -1), (2, 2, 2), "g")])

add("squid", "Squid Head", "Passive",
    pal={".": "#2c4a6c", "d": "#1b3049", "w": "#d8dde2", "k": K},
    front=["dddddddd",
           "d......d",
           "........",
           ".wk..kw.",
           "........",
           "........",
           "d.d..d.d",
           "........"])

add("strider", "Strider Head", "Passive",
    pal={".": "#a62d2d", "d": "#7a1f22", "k": "#1c1c1c", "h": "#6c5f6f"},
    front=["dddddddd",
           "........",
           "........",
           ".kk..kk.",
           "........",
           "........",
           "..kkkk..",
           "........"],
    extras=[Cube((-3, 8, -3), (1, 4, 1), "h"), Cube((0, 8, -1), (1, 3, 1), "h"),
            Cube((2, 8, 0), (1, 4, 1), "h"), Cube((-2, 8, 2), (1, 3, 1), "h")])

add("tadpole", "Tadpole Head", "Passive", size=(6, 4, 6),
    pal={".": "#5a3e2b", "k": K},
    front=["......", ".k..k.", "......", "......"])

add("tropicalfish", "Tropical Fish Head", "Passive", size=(6, 6, 6),
    pal={".": "#f08a2a", "w": "#f2f2f2", "k": K},
    front=["..ww..", "..ww..", "wk..kw", "..ww..", "......", "..ww.."],
    side=["..ww..", "..ww..", "..ww..", "..ww..", "..ww..", "..ww.."],
    extras=[Cube((-0.5, 6, -1), (1, 2, 3), "w")])

add("turtle", "Turtle Head", "Passive", size=(6, 5, 6),
    pal={".": "#5aa34a", "d": "#3d7a33", "k": K, "l": "#9fd08e"},
    front=["dddddd", "......", "k....k", "......", "llllll"])

VILLAGER_FRONT = ["........",
                  "........",
                  "........",
                  ".dddddd.",
                  ".wg..gw.",
                  "........",
                  "........",
                  "........",
                  "...mm...",
                  "........"]
add("villager", "Villager Head", "Passive", ["minecraft:villager_v2", "minecraft:villager"],
    size=(8, 10, 8),
    pal={".": "#bd8b72", "d": "#4a3020", "w": W, "g": "#2e8b3c", "m": "#7f5a48", "n": "#b07c62"},
    front=VILLAGER_FRONT,
    extras=[snout((8, 10, 8), (2, 4, 2), 2, "n")])

add("wandering_trader", "Wandering Trader Head", "Passive", size=(8, 10, 8),
    pal={".": "#bd8b72", "d": "#4a3020", "w": W, "g": "#2e8b3c", "m": "#7f5a48",
         "n": "#b07c62", "h": "#3a56a3"},
    front=["hhhhhhhh",
           "hh....hh",
           "h......h",
           "h.dddd.h",
           "hwg..gwh",
           "h......h",
           "h......h",
           "h......h",
           "h..mm..h",
           "h......h"],
    top_fill="h", side_fill="h", back_fill="h",
    extras=[snout((8, 10, 8), (2, 4, 2), 2, "n")])

add("zombie_horse", "Zombie Horse Head", "Passive", size=(6, 6, 6),
    pal={".": "#5f7d48", "d": "#3f5530", "l": "#6f8f56", "k": "#1a2412"},
    front=["dddddd", "......", "k....k", "......", "......", "......"],
    extras=[snout((6, 6, 6), (4, 4, 5), 0, "l", ["....", "....", "d..d", "...."])]
    + pair(-3, 6, 1, (1, 2, 1), "."))

add("sulfur_cube", "Sulfur Cube Head", "Passive",
    pal={".": "#cfd84a", "d": "#9aa22c", "k": "#2e3010"},
    front=["dddddddd",
           "d......d",
           "d.k..k.d",
           "d......d",
           "d..kk..d",
           "d......d",
           "d......d",
           "dddddddd"],
    experimental=True)

# --------------------------------------------------------------------------
# Neutral mobs
# --------------------------------------------------------------------------
add("bee", "Bee Head", "Neutral", size=(7, 7, 7),
    pal={".": "#f2c230", "k": "#1e1610", "b": "#5a3c1c"},
    front=[".......",
           ".......",
           "kk...kk",
           "kk...kk",
           ".......",
           "bbbbbbb",
           "......."],
    side=["..kk.kk"] * 7,
    extras=[Cube((-2, 7, -3), (1, 3, 1), "k"), Cube((1, 7, -3), (1, 3, 1), "k")])

add("dolphin", "Dolphin Head", "Neutral", size=(8, 7, 6),
    pal={".": "#7d8fa3", "l": "#c2ccd6", "k": K},
    front=["........", "........", "k......k", "........", "llllllll", "llllllll", "llllllll"],
    extras=[snout((8, 7, 6), (4, 2, 4), 0, "l")])

add("enderman", "Enderman Head", "Neutral",
    pal={".": "#161616", "p": "#cc00fa", "m": "#e079fa"},
    front=["........",
           "........",
           "........",
           "........",
           "mpp..ppm",
           "........",
           "........",
           "........"])

add("fox", "Fox Head", "Neutral", size=(8, 6, 6),
    pal={".": "#e37c30", "w": "#f2ece2", "k": "#1a1a1a", "d": "#b95b1d"},
    front=["dddddddd", "........", ".kk..kk.", "w......w", "ww....ww", "wwwwwwww"],
    extras=[snout((8, 6, 6), (4, 2, 3), 0, "w", [".kk.", "...."])]
    + pair(-4, 6, 0, (2, 2, 1), "d"))

add("goat", "Goat Head", "Neutral", size=(6, 6, 6),
    pal={".": "#e2ddd2", "d": "#bcb5a5", "k": K, "h": "#8f8a80"},
    front=["......", "......", "k....k", "......", "......", "......"],
    extras=[snout((6, 6, 6), (4, 3, 3), 2, "d", ["....", "k..k", "...."]),
            Cube((-1, 0, -5), (2, 2, 1), ".")]
    + pair(-3, 6, 0, (1, 4, 1), "h"))

add("iron_golem", "Iron Golem Head", "Neutral", size=(8, 10, 8),
    pal={".": "#cdc6bc", "d": "#9c958b", "k": "#2b2b2b", "r": "#b3202a", "g": "#4e7a2d"},
    front=["........",
           "g.......",
           ".dddddd.",
           ".rk..kr.",
           "g.......",
           "........",
           "........",
           "........",
           "...dd..g",
           "........"],
    extras=[snout((8, 10, 8), (2, 4, 2), 2, "d")])

LLAMA_EXTRAS = [snout((6, 6, 6), (4, 4, 4), 0)] + pair(-3, 6, 1, (2, 3, 1), ".")
add("llama", "Llama Head", "Neutral", size=(6, 6, 6),
    pal={".": "#e8dbb8", "d": "#c4b38a", "k": K},
    front=["dddddd", "......", "k....k", "......", "......", "......"],
    extras=LLAMA_EXTRAS)

add("trader_llama", "Trader Llama Head", "Neutral", size=(6, 6, 6),
    pal={".": "#e8dbb8", "d": "#c4b38a", "k": K, "b": "#2f5aa8", "y": "#e0b53a"},
    front=["dddddd", "......", "k....k", "bbbbbb", "yyyyyy", "......"],
    extras=LLAMA_EXTRAS)

add("panda", "Panda Head", "Neutral", size=(8, 7, 6),
    pal={".": "#f2f0ec", "k": "#1a1a1a", "w": W},
    front=["........", "........", ".kk..kk.", "kkw..wkk", ".kk..kk.", "........", "........"],
    extras=[snout((8, 7, 6), (4, 2, 2), 0, ".", [".kk.", "...."])]
    + pair(-4, 7, 0, (2, 2, 1), "k"))

add("polar_bear", "Polar Bear Head", "Neutral", size=(8, 7, 6),
    pal={".": "#f1f0ea", "k": K, "d": "#d8d6cc"},
    front=["........", "........", ".k....k.", "........", "........", "........", "........"],
    extras=[snout((8, 7, 6), (4, 3, 3), 0, "d", [".kk.", "....", "...."])]
    + pair(-4, 7, 1, (2, 2, 1), "."))

add("pufferfish", "Pufferfish Head", "Neutral",
    pal={".": "#e8c33a", "d": "#b88f1c", "k": K, "w": "#f2f2f2"},
    front=["d.d..d.d",
           "........",
           "wk....kw",
           "........",
           "...dd...",
           "........",
           "d......d",
           "........"],
    extras=pair(-5, 2, -1, (1, 1, 1), "w") + pair(-5, 6, -1, (1, 1, 1), "w")
    + pair(-2, 8, -1, (1, 1, 1), "w"))

add("wolf", "Wolf Head", "Neutral", size=(6, 6, 6),
    pal={".": "#d6d1cb", "d": "#a9a39c", "k": "#222222", "l": "#e7e3de"},
    front=["......", "......", "k....k", "......", "......", "......"],
    extras=[snout((6, 6, 6), (3, 3, 4), 0, "l", [".k.", "...", "..."])]
    + pair(-3, 6, 0, (2, 2, 1), "d"))

add("zombie_pigman", "Zombified Piglin Head", "Neutral", size=(10, 8, 8),
    pal={".": "#e39d95", "g": "#6a8a4a", "w": "#e8e2d0", "k": K, "n": "#c9877d", "d": "#a8645c"},
    front=["g.......ww",
           "........ww",
           "..........",
           "..wk..kw.w",
           "..........",
           "........g.",
           "..........",
           "g........."],
    extras=[snout((10, 8, 8), (4, 4, 1), 0, "n", ["....", "....", "d..d", "...."]),
            Cube((2, 1, -5), (1, 2, 1), "w")]
    + pair(-6, 3, -2, (1, 5, 4), "."))

# --------------------------------------------------------------------------
# Hostile mobs
# --------------------------------------------------------------------------
add("blaze", "Blaze Head", "Hostile",
    pal={".": "#f6c64b", "w": "#fff1a8", "o": "#d97a1a", "k": "#3b1a0a"},
    front=["wwwwwwww",
           "w......w",
           "........",
           ".kk..kk.",
           "........",
           "oo....oo",
           ".oooooo.",
           "o......o"])

add("bogged", "Bogged Skull", "Hostile",
    pal={".": "#8d9b6a", "d": "#5b6b3f", "k": "#1d2216", "g": "#4f7a2e", "r": "#b8322a", "m": "#8a6142"},
    front=["gg..g.gg",
           "g.......",
           "........",
           ".kk..kk.",
           ".kk..kk.",
           "...kk...",
           "..d.d.d.",
           "........"],
    extras=[Cube((0, 8, -1), (3, 2, 3), "r"), Cube((-3, 8, 1), (2, 2, 2), "m")])

add("breeze", "Breeze Head", "Hostile",
    pal={".": "#b8d9f2", "l": "#e6f4ff", "p": "#5c3e9e", "d": "#7fa6c8"},
    front=["llllllll",
           "l......l",
           "........",
           ".pp..pp.",
           "........",
           "...dd...",
           "........",
           "dddddddd"])

add("camel_husk", "Camel Husk Head", "Hostile", size=(6, 6, 6),
    pal={".": "#a58d64", "d": "#6f5b3a", "k": "#000000", "g": "#7c8a5a"},
    front=["g.....", "......", "k....k", "...g..", "......", "......"],
    extras=[snout((6, 6, 6), (4, 4, 4), 0, ".", ["....", "g...", "d..d", "...."])]
    + pair(-3, 6, 1, (1, 2, 1), "d"))

add("cave_spider", "Cave Spider Head", "Hostile",
    pal={".": "#103d3e", "d": "#0a2627", "r": "#c51b1b", "R": "#ff5a5a"},
    front=["........",
           "..r..r..",
           "........",
           ".rR..Rr.",
           ".rr..rr.",
           "........",
           "...dd...",
           "........"])

add("creaking", "Creaking Head", "Hostile",
    pal={".": "#4c3a2b", "d": "#2f241a", "o": "#ff8a1f", "y": "#ffd06a"},
    front=["d.d..d.d",
           "........",
           "d......d",
           ".oy..yo.",
           "........",
           "d.dddd.d",
           "..d..d..",
           "d......d"],
    extras=[Cube((-4, 8, -1), (1, 3, 1), "d"), Cube((2, 8, 1), (1, 2, 1), "d"),
            Cube((4, 6, 0), (2, 1, 1), "d")])

add("drowned", "Drowned Head", "Hostile",
    pal={".": "#4f9a8f", "d": "#2f6f6a", "c": "#7fe3e0", "k": "#16302c", "g": "#5b8a3a"},
    front=["dddddddd",
           "d.dd..dd",
           "........",
           ".cc..cc.",
           "........",
           "...gg...",
           "..kkkk..",
           "........"])

GUARDIAN_FRONT = ["dddddddd",
                  "d......d",
                  "d.wwww.d",
                  "d.wkkw.d",
                  "d.wkkw.d",
                  "d.wwww.d",
                  "d......d",
                  "dddddddd"]
GUARDIAN_SPIKES = ([Cube((x, 8, z), (1, 2, 1), "s") for x in (-3, 2) for z in (-3, 2)]
                   + pair(-6, 4, -0.5, (2, 1, 1), "s"))
add("elder_guardian", "Elder Guardian Head", "Hostile",
    pal={".": "#d1cbb4", "d": "#a39b80", "w": "#efe9f5", "k": "#7a4a8e", "s": "#f2ead8"},
    front=GUARDIAN_FRONT, extras=GUARDIAN_SPIKES)

add("endermite", "Endermite Head", "Hostile", size=(6, 4, 6),
    pal={".": "#3b2a4a", "d": "#251a30", "p": "#a67ac4"},
    front=["dddddd", "......", ".p..p.", "......"])

ILLAGER_FRONT = ["........",
                 "........",
                 ".dddddd.",
                 ".wg..gw.",
                 "........",
                 "........",
                 "..mmmm..",
                 "........"]
add("evoker", "Evoker Head", "Hostile", ["minecraft:evocation_illager"],
    pal={".": "#9aa3a3", "d": "#353535", "w": W, "g": "#2c8c3a", "m": "#6e7575",
         "n": "#8a9393", "r": "#1c1c1c", "y": "#d8b23a"},
    front=["rrrrrrrr", "r......r", ".dddddd.", ".wg..gw.", "........", "........", "..mmmm..", "yyyyyyyy"],
    extras=[snout((8, 8, 8), (2, 4, 2), 1, "n")])

add("ghast", "Ghast Head", "Hostile",
    pal={".": "#f0efef", "g": "#9a9a9a", "k": "#c8c8c8"},
    front=["........",
           "........",
           ".gg..gg.",
           "..k..k..",
           "........",
           "..gggg..",
           "........",
           "........"])

add("guardian", "Guardian Head", "Hostile",
    pal={".": "#5d9c8b", "d": "#3e6f63", "w": "#f2ead8", "k": "#e07b2b", "s": "#e7d9b8"},
    front=GUARDIAN_FRONT, extras=GUARDIAN_SPIKES)

HOGLIN_FRONT = ["hhhhhhhh", "........", "k......k", "........", "........", "........", "........"]
add("hoglin", "Hoglin Head", "Hostile", size=(8, 7, 8),
    pal={".": "#c58d6c", "d": "#8a5b40", "t": "#efe7d5", "k": K, "h": "#6b4a36"},
    front=HOGLIN_FRONT,
    extras=[snout((8, 7, 8), (6, 4, 2), 0, "d", ["......", "......", ".k..k.", "......"])]
    + pair(-4, 3, -6, (1, 3, 1), "t") + pair(-7, 6, -1, (3, 1, 2), "d"))

add("husk", "Husk Head", "Hostile",
    pal={".": "#b5a273", "d": "#8a7a50", "k": "#2b2414"},
    front=["dddddddd", "d......d", "........", ".kk..kk.", "........", "...dd...", "........", "........"])

add("magma_cube", "Magma Cube Head", "Hostile",
    pal={".": "#3a1610", "o": "#f07a1a", "y": "#ffd24a", "r": "#8a2a12"},
    front=["rr.or.rr",
           ".o....o.",
           "r......r",
           ".yy..yy.",
           "..o..o..",
           "r......r",
           ".r.oo.r.",
           "r......r"],
    side=["r..o..r.", "........", ".o...r..", "........", "r....o..", "........", "..r....o", "........"])

add("parched", "Parched Skull", "Hostile",
    pal={".": "#d8c39a", "d": "#a99169", "k": "#3a2a14"},
    front=["d..d....",
           "......d.",
           "........",
           ".kk..kk.",
           ".kk..kk.",
           "...kk...",
           "..d.d.d.",
           "........"])

add("phantom", "Phantom Head", "Hostile", size=(8, 4, 7),
    pal={".": "#435089", "l": "#6f80b8", "g": "#8bff4f"},
    front=["llllllll", "........", "gg....gg", "........"])

add("piglin_brute", "Piglin Brute Head", "Hostile", size=(10, 8, 8),
    pal={".": "#e3a08e", "d": "#b8745e", "k": K, "w": W, "g": "#d6b33c", "b": "#2a2a2a", "n": "#e9b3a5"},
    front=["bbbbbbbbbb",
           "gggggggggg",
           "..........",
           "..wk..kw..",
           "..........",
           "..........",
           "..........",
           ".........."],
    top_fill="b",
    extras=[snout((10, 8, 8), (4, 4, 1), 0, "n", ["....", "....", "d..d", "...."])]
    + pair(-3, 1, -5, (1, 2, 1), "w") + pair(-6, 3, -2, (1, 5, 4), "."))

add("pillager", "Pillager Head", "Hostile",
    pal={".": "#9aa3a3", "d": "#2a2a2a", "w": W, "g": "#2c8c3a", "m": "#5c6363", "n": "#8a9393", "b": "#6c7373"},
    front=["........", "........", ".dddddd.", ".wg..gw.", "........", "b.b..b.b", ".bmmmmb.", "b.b..b.b"],
    extras=[snout((8, 8, 8), (2, 4, 2), 1, "n")])

add("ravager", "Ravager Head", "Hostile",
    pal={".": "#5b5a55", "d": "#3b3a37", "k": K, "w": "#dddddd", "b": "#8f7a5d"},
    front=["dddddddd", "........", ".dddddd.", ".wk..kw.", "........", "........", "........", "dddddddd"],
    extras=[snout((8, 8, 8), (4, 4, 2), 0, ".", ["....", "....", "k..k", "...."])]
    + pair(-6, 6, -1, (2, 1, 1), "b") + pair(-6, 7, -1, (1, 3, 1), "b"))

add("shulker", "Shulker Head", "Hostile",
    pal={".": "#915f91", "d": "#6b436b", "y": "#e8dd85", "k": K},
    front=["........",
           "........",
           "dddddddd",
           "d.yyyy.d",
           "d.kyyk.d",
           "d.yyyy.d",
           "dddddddd",
           "........"])

add("silverfish", "Silverfish Head", "Hostile", size=(6, 4, 6),
    pal={".": "#8b8b8b", "d": "#5d5d5d", "k": K},
    front=["dddddd", "......", ".k..k.", "d....d"])

add("slime", "Slime Head", "Hostile",
    pal={".": "#79c05a", "d": "#4f8d3a", "l": "#a7df8a"},
    front=["llllllll",
           "l......l",
           ".dd..dd.",
           ".dd..dd.",
           "........",
           "....d...",
           "........",
           "........"])

add("spider", "Spider Head", "Hostile",
    pal={".": "#3a302c", "d": "#231c19", "r": "#c51b1b", "R": "#ff5a5a"},
    front=["........",
           "..r..r..",
           "........",
           ".rR..Rr.",
           ".rr..rr.",
           "........",
           "...dd...",
           "........"])

add("stray", "Stray Skull", "Hostile",
    pal={".": "#a9b5b7", "d": "#7e8c8f", "k": "#1d2a2c", "i": "#cfe3e8"},
    front=["iiiiiiii",
           "i......i",
           "........",
           ".kk..kk.",
           ".kk..kk.",
           "...kk...",
           "..d.d.d.",
           "........"],
    top_fill="i")

add("vex", "Vex Head", "Hostile",
    pal={".": "#9fadbc", "d": "#6c7d90", "k": K, "w": "#dfe8f2"},
    front=["dddddddd", "d......d", "........", ".kw..wk.", "........", "..kkkk..", "...kk...", "........"],
    extras=pair(-5, 2, 2, (1, 5, 2), "w"))

add("vindicator", "Vindicator Head", "Hostile",
    pal={".": "#a3abab", "d": "#1a1a1a", "w": W, "g": "#2c8c3a", "m": "#6e7575", "n": "#929b9b"},
    front=ILLAGER_FRONT,
    extras=[snout((8, 8, 8), (2, 4, 2), 1, "n")])

add("warden", "Warden Head", "Hostile",
    pal={".": "#0f4250", "d": "#0a2d37", "c": "#5ff0f0", "k": "#071c22"},
    front=["dddddddd", "d......d", "........", "c......c", "........", "..kkkk..", "..k..k..", "........"],
    extras=pair(-8, 4, -1, (4, 5, 1), "c"))

add("witch", "Witch Head", "Hostile", size=(8, 10, 8),
    pal={".": "#a98c79", "d": "#3a2a2a", "w": W, "g": "#4aa045", "m": "#6e5446",
         "n": "#9c7f6d", "h": "#352347"},
    front=VILLAGER_FRONT,
    extras=[snout((8, 10, 8), (2, 4, 2), 1, "n"), Cube((0, 2, -7), (1, 1, 1), "g"),
            Cube((-5, 10, -5), (10, 1, 9), "h"), Cube((-3, 11, -3), (6, 3, 6), "h"),
            Cube((-1.5, 14, -1.5), (3, 2, 3), "h")])

add("zoglin", "Zoglin Head", "Hostile", size=(8, 7, 8),
    pal={".": "#d9a6a0", "d": "#a46d6a", "t": "#f3eee0", "k": K, "h": "#c9d6c0"},
    front=HOGLIN_FRONT,
    extras=[snout((8, 7, 8), (6, 4, 2), 0, "d", ["......", "......", ".k..k.", "......"])]
    + pair(-4, 3, -6, (1, 3, 1), "t") + pair(-7, 6, -1, (3, 1, 2), "d"))

add("zombie_nautilus", "Zombie Nautilus Head", "Hostile",
    pal={".": "#a9b39a", "s": "#5e7a4a", "k": "#2b3d22", "t": "#7d9a6a"},
    front=["s.s.s.s.",
           "........",
           "ss.ss.ss",
           "........",
           "k......k",
           "tttttttt",
           "t.tt.tt.",
           "t.t..t.t"],
    side=["s.s.s.s.", "........", "ss.ss.ss", "........",
          "s.s.s.s.", "........", "ss.ss.ss", "........"])

add("zombie_villager", "Zombie Villager Head", "Hostile",
    ["minecraft:zombie_villager_v2", "minecraft:zombie_villager"], size=(8, 10, 8),
    pal={".": "#5d8c49", "d": "#2c4a22", "w": W, "g": "#9b1b1b", "m": "#3d5c30", "n": "#4d7a3c"},
    front=VILLAGER_FRONT,
    extras=[snout((8, 10, 8), (2, 4, 2), 2, "n")])

# --------------------------------------------------------------------------
# Bosses
# --------------------------------------------------------------------------
add("wither", "Wither Head", "Boss",
    pal={".": "#2b2b2b", "d": "#141414", "w": "#e0e0e0"},
    front=["dddddddd", "d......d", "........", ".ww..ww.", ".dd..dd.", "........", "..d.d.d.", "........"])
