"""Head art: Hostile mobs, part 2 (magma cube to zombie villager) and bosses.

See tools/mobs.py for the coordinate system and the art conventions.
"""

from mobs import K, W, Cube, V, add, pair, snout  # noqa: F401


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

ILLAGER_FRONT = ["........",
                 "........",
                 ".dddddd.",
                 ".wg..gw.",
                 "........",
                 "........",
                 "..mmmm..",
                 "........"]

HOGLIN_FRONT = ["hhhhhhhh", "........", "k......k", "........", "........", "........", "........"]

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

add("wither", "Wither Head", "Boss",
    pal={".": "#2b2b2b", "d": "#141414", "w": "#e0e0e0"},
    front=["dddddddd", "d......d", "........", ".ww..ww.", ".dd..dd.", "........", "..d.d.d.", "........"])
