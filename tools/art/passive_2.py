"""Head art: Passive mobs, part 2 (mooshroom to zombie horse, plus bonus heads).

See tools/mobs.py for the coordinate system and the art conventions.
"""

from mobs import K, W, Cube, V, add, pair, snout  # noqa: F401


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
