"""Head art: Neutral mobs.

See tools/mobs.py for the coordinate system and the art conventions.
"""

from mobs import K, W, Cube, V, add, pair, snout  # noqa: F401


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
