"""Head art: Passive mobs, part 1 (allay to horse).

See tools/mobs.py for the coordinate system and the art conventions.
"""

from mobs import K, W, Cube, V, add, pair, snout  # noqa: F401


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

# Vanilla chicken head: 4x6x3 with a 4x2x2 beak and a 2x2x1 red wattle.
# The cold chicken adds a fluffy 6x3x4 cap over the top of its head.
CHICKEN = (4, 6, 3)
CHICKEN_BEAK = snout(CHICKEN, (4, 2, 2), 2, "y",
                     faces={"front": ["yyyy", "oooo"], "top": ["yyyy", "YYYY"],
                            "side": ["yy", "oo"]})
CHICKEN_WATTLE = snout(CHICKEN, (2, 2, 1), 0, "r", faces={"front": ["rr", "rR"]})
add("chicken", "Chicken Head", "Passive", size=CHICKEN,
    pal={".": W, "s": "#dcdcdc", "S": "#c4c4c4", "k": K, "e": "#3a3a3a",
         "y": "#e8a92b", "Y": "#f6c552", "o": "#c07d18", "r": "#cc2a2a", "R": "#9e1c1c"},
    front=["s..s",
           "k..k",
           "....",
           "....",
           "s..s",
           "sSSs"],
    side=["...",
          "..e",
          "...",
          "s..",
          "ss.",
          "SSs"],
    top=["s..s",
         "....",
         "...."],
    back=["....",
          "....",
          "s..s",
          "....",
          "ssss",
          "SSSS"],
    extras=[CHICKEN_BEAK, CHICKEN_WATTLE],
    variants=[
        V("temperate", "Chicken Head", {"minecraft:climate_variant": "temperate"}),
        V("warm", "Warm Chicken Head", {"minecraft:climate_variant": "warm"},
          pal={".": "#d08a4a", "s": "#b8703a", "S": "#97562a", "e": "#2a1a10"},
          top=["sSSs",
               "s..s",
               "...."]),
        V("cold", "Cold Chicken Head", {"minecraft:climate_variant": "cold"},
          pal={".": "#8f7f70", "s": "#76675a", "S": "#5e5248", "e": "#1f1a16",
               "c": "#efe6d6", "C": "#d6c8b0", "f": "#fff8ec"},
          extras=[CHICKEN_BEAK, CHICKEN_WATTLE,
                  Cube((-3, 4, -1.5), (6, 3, 4), "c",
                       faces={"front": ["fcfcfc", "cCcfcC", "C.CC.C"],
                              "side": ["cfcf", "CcCc", "C.C."],
                              "top": ["fcfcfc", "cfcfcf", "fcfcfc", "cfcfcf"],
                              "back": ["cfcfcf", "CcCcCc", "C.CC.C"]})]),
    ])

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
