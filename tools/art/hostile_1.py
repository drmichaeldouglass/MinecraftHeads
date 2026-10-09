"""Head art: Hostile mobs, part 1 (blaze to husk).

See tools/mobs.py for the coordinate system and the art conventions.
"""

from mobs import K, W, Cube, V, add, pair, snout  # noqa: F401


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
