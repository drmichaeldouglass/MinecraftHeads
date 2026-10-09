"""Head art: Passive mobs, part 2 (mooshroom to zombie horse, plus bonus heads).

See tools/mobs.py for the coordinate system and the art conventions.
"""

from mobs import K, W, Cube, V, add, pair, snout  # noqa: F401


def paint(art, rows):
    """Copy of art with some rows replaced: rows is {row index: new row}."""
    return [rows.get(i, row) for i, row in enumerate(art)]


# --------------------------------------------------------------------------
# Mooshroom: vanilla 8x8x6 head, 6x3x1 muzzle, 1x3x1 horns and a mushroom
# growing out of the top of the head.
# --------------------------------------------------------------------------
MOOSHROOM = (8, 8, 6)
MOOSHROOM_MUZZLE = snout(MOOSHROOM, (6, 3, 1), 0, "m",
                         faces={"front": ["MmmmmM", "mn..nm", "MMmmMM"],
                                "top": ["MmmmmM"], "side": ["M", ".", "M"]})
MOOSHROOM_HORNS = pair(-5, 6, -1, (1, 3, 1), "h",
                       faces={"front": ["H", ".", "."], "side": ["H", ".", "."],
                              "back": ["H", ".", "I"], "top": ["H"]})
MOOSHROOM_STEM = Cube((-1, 8, -1), (2, 2, 2), "t",
                      faces={"front": ["..", "TT"], "side": ["..", "TT"], "back": ["..", "TT"]})
RED_MUSHROOM = [MOOSHROOM_STEM,
                Cube((-2, 10, -2), (4, 2, 4), "r",
                     faces={"front": [".s..", "R..s"], "side": ["..s.", "s..R"],
                            "back": ["s...", "..sR"], "top": [".s..", "...s", "s...", "..s."]}),
                Cube((-1, 12, -1), (2, 1, 2), "r",
                     faces={"front": ["s."], "side": [".s"], "top": ["s.", ".s"]})]
BROWN_MUSHROOM = [MOOSHROOM_STEM,
                  Cube((-2.5, 10, -2.5), (5, 1, 5), "b",
                       faces={"front": ["BbBbB"], "side": ["bBbBb"], "back": ["BbBbB"],
                              "top": ["c...c", ".c.c.", "..c..", ".c.c.", "c...c"]}),
                  Cube((-1.5, 11, -1.5), (3, 1, 3), "b",
                       faces={"front": ["cBc"], "side": ["BcB"], "back": ["cBc"],
                              "top": [".c.", "c.c", ".c."]})]

add("mooshroom", "Mooshroom Head", "Passive", size=MOOSHROOM,
    pal={".": "#a8231d", "d": "#7c1813", "l": "#c63a2e", "w": "#e4dedb", "W": "#c4bab5",
         "k": K, "e": "#f2f2f2", "m": "#c2b6ad", "M": "#a29489", "n": "#4d403a",
         "h": "#ddd5c4", "H": "#9b927f", "I": "#bdb4a2",
         "r": "#d8261e", "R": "#a81a14", "s": "#f4eee8", "t": "#e8e0d0", "T": "#c4b9a6",
         "b": "#9a6d4a", "B": "#76512f", "c": "#b88a62"},
    front=["dd.ll.dd",
           "d.wwww.d",
           "...wW...",
           "ke.ww.ek",
           "l..ww..l",
           "d......d",
           "d......d",
           "dd.dd.dd"],
    side=["dd.ddd",
          ".ww..l",
          "wWWw..",
          "wwWww.",
          ".www.l",
          "l.....",
          "d....d",
          "dd.ddd"],
    top=["dd.dd.dd",
         "..wwww..",
         ".wwWWww.",
         "..wwww..",
         "........",
         "l.llll.l"],
    back=["dddddddd",
          "..www...",
          ".wwWWw..",
          ".wWWwww.",
          "..www..w",
          "l.....ww",
          "d....wWw",
          "dd.dddww"],
    extras=[MOOSHROOM_MUZZLE] + MOOSHROOM_HORNS + RED_MUSHROOM,
    variants=[
        V("red", "Red Mooshroom Head", {"variant": 0}),
        V("brown", "Brown Mooshroom Head", {"variant": 1},
          pal={".": "#a5714a", "d": "#7d5232", "l": "#bf8b60", "w": "#ebe4dc",
               "W": "#cbbfb2"},
          extras=[MOOSHROOM_MUZZLE] + MOOSHROOM_HORNS + BROWN_MUSHROOM),
    ])


# --------------------------------------------------------------------------
# Horse family (mule, skeleton horse, zombie horse): vanilla horse v3 head,
# a 6x5x7 skull with a 4x5x5 muzzle, ears at the back and a short mane tuft.
# Eyes sit on the sides of the skull, as on the real horse.
# --------------------------------------------------------------------------
HORSE = (6, 5, 6)


def horse(key, name, pal, side, top, back, muzzle, ear_size, mane=True, ear=None):
    ear = ear or [".."] + [".d"] * (ear_size[1] - 2) + [".."]
    extras = [snout(HORSE, (4, 5, 5), 0, "m", faces=muzzle)]
    extras += pair(-3, 5, 2, ear_size, ".", faces={"front": ear, "back": [".."] * ear_size[1],
                                                   "top": ["d."]})
    if mane:
        extras.append(Cube((-1, 5, -0.5), (2, 1, 4), "M",
                           faces={"top": ["N.", ".N", "N.", ".N"], "front": ["NN"],
                                  "side": [".N.N"], "back": ["N."]}))
    add(key, name, "Passive", size=HORSE, pal=pal,
        front=["d....d", "......", "......", "......", "d....d"],
        side=side, top=top, back=back, extras=extras)


horse("mule", "Mule Head",
      pal={".": "#5e4030", "d": "#45301f", "l": "#77553f", "k": "#140d08", "e": "#4a3a30",
           "m": "#8c7563", "n": "#2b1e16", "o": "#6e5a4b",
           "M": "#2f2018", "N": "#46301f"},
      side=["dd...l",
            "d...ek",
            "d....l",
            "d.....",
            "dd..ll"],
      top=["dd..dd",
           "d....d",
           "......",
           "..ll..",
           "......",
           "l....l"],
      back=["dddddd",
            "d....d",
            "......",
            "......",
            "dddddd"],
      muzzle={"front": ["....", "n..n", "....", "....", "onno"],
              "side": ["l....", ".....", ".....", "..nnn", "ooooo"],
              "top": ["....", "....", "o..o", "....", "...."]},
      ear_size=(2, 6, 1))

horse("skeleton_horse", "Skeleton Horse Head",
      pal={".": "#d9d5c4", "d": "#aaa592", "l": "#eeeadb", "k": "#262421", "e": "#4a463e",
           "m": "#d9d5c4", "n": "#2e2c28", "t": "#f4f1e6", "o": "#aaa592"},
      side=["d.d.l.",
            "d..kk.",
            "...ke.",
            "d.d...",
            "ddd.dd"],
      top=["d.dd.d",
           "......",
           ".d..d.",
           "..dd..",
           "......",
           "l.ll.l"],
      back=["dd..dd",
            "d.kk.d",
            "..kk..",
            "d....d",
            "dddddd"],
      muzzle={"front": ["l..l", "nn.n", "n...", "tttt", "ooto"],
              "side": ["..l..", "....n", ".....", "tntnt", "ooooo"],
              "top": ["d..d", ".dd.", "....", "ln.l", "nn.n"]},
      ear_size=(2, 3, 1), mane=False)

horse("zombie_horse", "Zombie Horse Head",
      pal={".": "#5b7a45", "d": "#405a2f", "l": "#78965c", "k": "#151d10", "e": "#7a1f1f",
           "m": "#6c8656", "n": "#24301a", "o": "#4c623a", "r": "#3b4a2c", "b": "#8a7a5a",
           "M": "#2d3a20", "N": "#3f2f20"},
      side=["dd.r.l",
            "d..rek",
            "..r..l",
            "d.rr..",
            "dd.dll"],
      top=["dd.rdd",
           "d...rd",
           ".r....",
           ".rr.l.",
           "......",
           "l.r..l"],
      back=["ddrddd",
            "d.rr.d",
            "...r..",
            ".r....",
            "dddddd"],
      muzzle={"front": ["..r.", "n..n", ".r..", "....", "onno"],
              "side": ["l.r..", "...r.", ".r...", "..nnn", "ooobo"],
              "top": ["..r.", ".rr.", "o..o", "r...", "...."]},
      ear_size=(2, 3, 1))


# --------------------------------------------------------------------------
# Nautilus: the whole mob is the trophy. A striped spiral shell with the soft
# body, big eyes and tentacles poking out of the front.
# --------------------------------------------------------------------------
add("nautilus", "Nautilus Head", "Passive", size=(10, 10, 8),
    pal={".": "#ece2cf", "c": "#d6c8ae", "s": "#bf6a2e", "S": "#8e4520", "o": "#e08a4a",
         "u": "#3a2418", "b": "#a8786a", "B": "#7e5448", "p": "#c99888", "k": K,
         "y": "#e8c860"},
    front=["..s.ss.s..",
           ".s.s..s.s.",
           "s.s.ss.s.s",
           "c.s....s.c",
           "Sc......cS",
           "uu......uu",
           "uu......uu",
           "uu......uu",
           "uu......uu",
           "SuuuuuuuuS"],
    side=["..ssss..",
          ".s....s.",
          "s.oSSo.s",
          "s.S..S.s",
          "s.S.Ss.s",
          "s.So.s.c",
          ".s..s..c",
          "c.ss..cS",
          "cc...cSu",
          "SccccSuu"],
    top=["c.s..s..sc",
         ".s..s..s..",
         ".s..s..s..",
         "s..s..s..s",
         ".s..s..s..",
         ".s..s..s..",
         "c.s..s..sc",
         "s.s.ss.s.s"],
    back=["..ssssss..",
          ".s......s.",
          "s..oSSo..s",
          "s.S....S.s",
          "s.S.SS.S.s",
          "s.S.So.S.s",
          "s..S..S..s",
          ".s..SS..s.",
          "c.s....s.c",
          "cc.ssss.cc"],
    extras=[
        # The leathery hood over the body, then the body with eyes and
        # tentacles, sitting in the mouth of the shell.
        snout((10, 10, 8), (8, 1, 2), 5, "B",
              faces={"front": ["BbBbbBbB"], "top": ["BbBbbBbB", "bBbBBbBb"]}),
        snout((10, 10, 8), (8, 5, 1), 0, "b",
              faces={"front": ["BkyBByk.",
                               "bkkbbkkb",
                               "pbpbbpbp",
                               "pbpbpbpb",
                               "BpBpBpBp"],
                     "top": ["bBbbbbBb"], "side": ["B", "k", ".", "p", "B"]}),
    ])


# --------------------------------------------------------------------------
# Ocelot: vanilla 5x4x5 head scaled to 6x5x6, with the 3x2x2 muzzle and the
# small ears. Yellow fur with dark rosette spots, green eyes.
# --------------------------------------------------------------------------
add("ocelot", "Ocelot Head", "Passive", size=(6, 5, 6),
    pal={".": "#e6c060", "d": "#c99a3a", "s": "#5e3f1c", "l": "#f3dfa0", "g": "#58b448",
         "k": K, "p": "#e08a86", "n": "#3c2818"},
    front=["s.ss.s",
           "......",
           "gk..kg",
           "l....l",
           "ll..ll"],
    side=["s..s.s",
          ".s....",
          "...s.g",
          "s.s..l",
          ".d.dll"],
    top=["s.s..s",
         ".s..s.",
         "..ss..",
         "s....s",
         ".s..s.",
         "s.ss.s"],
    back=["s.ss.s",
          ".s..s.",
          "s....s",
          "..ss..",
          "dd..dd"],
    extras=[snout((6, 5, 6), (4, 2, 2), 0, "l",
                  faces={"front": [".pp.", "n..n"], "top": ["....", "d..d"],
                         "side": ["..", "d."]})]
    + pair(-3, 5, 0, (2, 1, 2), ".",
           faces={"front": ["sp"], "top": ["s.", ".."], "side": ["s."], "back": ["ss"]}))


# --------------------------------------------------------------------------
# Parrot: the tiny vanilla head (2x3x2 with a 2x1x4 crown, a two-part hooked
# beak and a feather crest) scaled up twice.
# --------------------------------------------------------------------------
PARROT = (4, 6, 4)
PARROT_EXTRAS = [
    # Crown: the top of the head reaching forward over the beak.
    Cube((-2, 6, -5), (4, 2, 7), ".",
         faces={"front": ["dbbd", "lbbl"],
                "side": ["d.....l", "....ldl"],
                "top": ["d..d", ".dd.", "....", "....", "....", ".bb.", "dbbd"],
                "back": ["dddd", "d..d"]}),
    # Upper beak, then the hooked tip hanging under the crown.
    Cube((-1, 2, -4), (2, 4, 2), "b",
         faces={"front": ["..", "..", "B.", "BB"], "side": ["..", "..", ".B", "BB"]}),
    Cube((-1, 3, -5), (2, 3, 1), "b",
         faces={"front": ["..", "..", "BB"], "side": [".", ".", "B"]}),
    # Feather crest sweeping back.
    Cube((-0.5, 8, -1), (1, 2, 4), "c", faces={"side": ["c.c.", ".c.c"]}),
    Cube((-0.5, 10, 1), (1, 2, 3), "c", faces={"side": ["c..", ".c."]}),
]


def parrot_pal(body, dark, crest, face, cheek, light):
    return {".": body, "d": dark, "c": crest, "f": face, "y": cheek, "l": light}


add("parrot", "Parrot Head", "Passive", size=PARROT,
    pal={**parrot_pal("#d8251c", "#a5150f", "#e8473a", "#ececec", "#d8251c", "#ec5a4a"),
         "k": K, "b": "#3a3a3a", "B": "#232323"},
    front=["f..f",
           "ff.f",
           "f..f",
           "yffy",
           "yyyy",
           "ldld"],
    side=["dl..",
          "..fk",
          "..ff",
          "..yf",
          "d.yy",
          "ddll"],
    top=["dlld",
         "....",
         "....",
         "...."],
    back=["dldl",
          "....",
          "d..d",
          "....",
          "dddd",
          "dldd"],
    extras=PARROT_EXTRAS,
    variants=[
        V("red", "Red Parrot Head", {"variant": 0}),
        V("blue", "Blue Parrot Head", {"variant": 1},
          pal=parrot_pal("#2d5bd2", "#1c3c94", "#4a78e6", "#f0f0f0", "#f0c832", "#5b86ea")),
        V("green", "Green Parrot Head", {"variant": 2},
          pal=parrot_pal("#5cba26", "#3c8a16", "#7ad23e", "#e8ead0", "#e04a2a", "#8ed85a")),
        V("cyan", "Cyan Parrot Head", {"variant": 3},
          pal=parrot_pal("#2bbad6", "#1a8aa2", "#f0cf2a", "#f2f2f2", "#f0cf2a", "#70d8ea")),
        V("gray", "Gray Parrot Head", {"variant": 4},
          pal={**parrot_pal("#a7a7a7", "#7c7c7c", "#d8d8d8", "#ededed", "#ededed", "#c4c4c4"),
               "b": "#4a4a4a", "B": "#2e2e2e"}),
    ])


# --------------------------------------------------------------------------
# Pig: vanilla 8x8x8 head with the 4x3x1 snout. Climate variants: the warm
# pig is a muddy rust colour, the cold pig grows a shaggy coat on its head.
# --------------------------------------------------------------------------
PIG_SNOUT = snout((8, 8, 8), (4, 3, 1), 1, "n",
                  faces={"front": ["l..l", "N..N", "...."], "top": ["llll"],
                         "side": ["l", "N", "."]})
add("pig", "Pig Head", "Passive",
    pal={".": "#f0a5a2", "d": "#d9817f", "l": "#f8c4c0", "k": K, "w": W,
         "n": "#f6b5b1", "N": "#a4504d", "c": "#7a5e4e", "C": "#a3826c", "e": "#5a4438"},
    front=["l.....d.",
           "..d.....",
           "......l.",
           ".l......",
           "kw....wk",
           "........",
           "d......d",
           "dd....dd"],
    side=["d.....l.",
          "..l.....",
          ".....d..",
          "d.......",
          "..d...l.",
          ".......d",
          "d.l.....",
          "dd...ddd"],
    top=["..l...d.",
         "d.....l.",
         "...d....",
         ".l....d.",
         "....l...",
         "..d.....",
         "d.....l.",
         "l..l...."],
    back=["....l...",
          ".d.....d",
          "...l....",
          "d.....l.",
          "..d.....",
          ".....d..",
          "l.......",
          "dd....dd"],
    extras=[PIG_SNOUT],
    variants=[
        V("temperate", "Pig Head", {"minecraft:climate_variant": "temperate"}),
        V("warm", "Warm Pig Head", {"minecraft:climate_variant": "warm"},
          pal={".": "#b8673e", "d": "#7e3f22", "l": "#d08a5c", "n": "#c87a52",
               "N": "#5a2814"},
          front=["d.d...d.",
                 "dd.d..dd",
                 "......l.",
                 ".l......",
                 "kw....wk",
                 "........",
                 "d......d",
                 "dd....dd"],
          side=["dd.d..l.",
                ".dd.....",
                ".....dd.",
                "d....dd.",
                "..d...l.",
                "......dd",
                "ddl.....",
                "dd...ddd"],
          top=["dd.l..dd",
               "d...ddl.",
               "...dd...",
               ".l....dd",
               "dd..l..d",
               ".dd.....",
               "d.....ld",
               "l..l..d."],
          back=["dd..l.dd",
                ".dd....d",
                "...l.dd.",
                "dd....l.",
                ".dd.....",
                "....dd..",
                "l...dd..",
                "dd....dd"]),
        V("cold", "Cold Pig Head", {"minecraft:climate_variant": "cold"},
          pal={".": "#e8a29b", "d": "#cf827b", "l": "#f4c0b8"},
          extras=[PIG_SNOUT,
                  Cube((-4.5, 6, -4.5), (9, 3, 9), "c",
                       faces={"front": ["CcCcecCcC", "c.c.C.c.c", ".e.c.c.e."],
                              "side": ["cCcCcCcCc", ".c.Cc.c.e", "e.c..e.c."],
                              "back": ["cCcCcCcCc", "c.ec.Cc.c", ".c.e.c.e."],
                              "top": ["cCc.cCc.c", ".c.Cc.cC.", "Cc.c.c.cC",
                                      "c.CcC.c.c", ".c.c.cCc.", "cC.c.C.cC",
                                      "c.cCc.c.c", ".Cc.c.cC.", "cCc.cCc.c"]})]),
    ])


# --------------------------------------------------------------------------
# Rabbit: vanilla 5x5x5 head grown to 6x5x5, with the tall 2x5x1 ears and a
# small muzzle. Six coat colours.
# --------------------------------------------------------------------------
RABBIT = (6, 5, 5)
RABBIT_MUZZLE = snout(RABBIT, (2, 2, 1), 1, "m",
                      faces={"front": ["pp", "M."], "top": ["pp"], "side": ["p", "."]})
RABBIT_EARS = pair(-3, 5, 0.5, (2, 5, 1), ".",
                   faces={"front": ["d.", "e.", "e.", "e.", "d."],
                          "back": ["d.", "..", "..", ".d", "dd"], "top": ["d."]})
RABBIT_ART = dict(
    front=["d.l..d",
           "kl..lk",
           "l....l",
           "lm..ml",
           ".mmmm."],
    side=["d.l.l",
          ".d..k",
          ".l..l",
          "d...m",
          "d.mmm"],
    top=["d.dd.d",
         ".d..d.",
         "..ll..",
         "l....l",
         ".l..l."],
    back=["d.dd.d",
          ".d..d.",
          "d....d",
          ".d..d.",
          "dd..dd"],
)
# Black and white (Dutch) rabbit: black ears, eye patches and back of the
# head, with a white blaze down the middle.
RABBIT_DUTCH = dict(
    front=["xx..xx",
           "kx..xk",
           "xx..xx",
           ".m..m.",
           ".mmmm."],
    side=["xxxxx",
          "xxxxk",
          "xxxxx",
          "xxx.m",
          "x.mmm"],
    top=["xxxxxx",
         "xxxxxx",
         "xx..xx",
         "xx..xx",
         "xx..xx"],
    back=["xxxxxx",
          "xxxxxx",
          "xxxxxx",
          "xxxxxx",
          "xx..xx"],
    extras=[RABBIT_MUZZLE] + pair(-3, 5, 0.5, (2, 5, 1), "x",
                                  faces={"front": ["X.", "e.", "e.", "e.", "X."],
                                         "back": ["X.", "..", "..", ".X", "XX"],
                                         "top": ["X."]}),
)

add("rabbit", "Rabbit Head", "Passive", size=RABBIT,
    pal={".": "#8c6a4b", "d": "#6b4e36", "l": "#a8865f", "m": "#e2d4bf", "M": "#b8a690",
         "k": K, "e": "#e8a0a8", "p": "#e08a96", "x": "#262220", "X": "#121010"},
    **RABBIT_ART,
    extras=[RABBIT_MUZZLE] + RABBIT_EARS,
    variants=[
        V("brown", "Brown Rabbit Head", {"variant": 0}),
        V("white", "White Rabbit Head", {"variant": 1},
          pal={".": "#eeece8", "d": "#d2cec8", "l": "#ffffff", "m": "#f8f6f2",
               "M": "#d8d2ca", "k": "#a8343c"}),
        V("black", "Black Rabbit Head", {"variant": 2},
          pal={".": "#2e2925", "d": "#1c1916", "l": "#45403a", "m": "#5e5650",
               "M": "#3a3430", "e": "#b0707a", "p": "#c08088", "k": "#0a0a0a"}),
        V("black_and_white", "Black and White Rabbit Head", {"variant": 3},
          pal={".": "#eeece8", "d": "#d2cec8", "l": "#ffffff", "m": "#f8f6f2",
               "M": "#d8d2ca", "k": "#d8d2ca"},
          **RABBIT_DUTCH),
        V("gold", "Gold Rabbit Head", {"variant": 4},
          pal={".": "#e6c886", "d": "#c8a45e", "l": "#f4e0ac", "m": "#faf0da",
               "M": "#dcc8a2"}),
        V("salt_and_pepper", "Salt and Pepper Rabbit Head", {"variant": 5},
          pal={".": "#8e7f70", "d": "#4e443c", "l": "#c8bcae", "m": "#bdb0a2",
               "M": "#7a6c60"},
          front=["dl.dld",
                 "kld.lk",
                 "l.d.ld",
                 "lm..ml",
                 "dmmmmd"],
          side=["dl.ll",
                "l.d.k",
                ".dldl",
                "dl..m",
                "d.mmm"],
          top=["dl.d.d",
               ".dl.dl",
               "l..ld.",
               "d.ld.l",
               ".ld.l."],
          back=["d.ld.d",
                "ld.l.l",
                "d.l.dd",
                ".dl.d.",
                "dd.ldd"]),
    ])


# --------------------------------------------------------------------------
# Salmon: the front of the fish scaled up twice. A 6x8x4 slice of body with
# the 4x6x3 head in front, a top fin and two small side fins.
# --------------------------------------------------------------------------
add("salmon", "Salmon Head", "Passive", size=(6, 8, 4),
    pal={".": "#b0473a", "d": "#86322a", "g": "#4f6a55", "G": "#3a5040", "l": "#d07a5a",
         "w": "#e8dcc8", "k": K, "m": "#5a1a14", "f": "#c86a44", "s": "#2e3a30"},
    front=["gGGGGg",
           "gGggGg",
           "g....g",
           "......",
           "d....d",
           "......",
           "l....l",
           "llllll"],
    side=["GgGg",
          "gsgg",
          "g.s.",
          "..s.",
          ".d..",
          "...d",
          "l.l.",
          "llll"],
    top=["GgsG.G",
         "gGgsGg",
         "GsgGgs",
         "gGgGsG"],
    back=["GgGGgG",
          "gGsgGg",
          "g.gg.g",
          "......",
          "d.s..d",
          "......",
          "l....l",
          "llllll"],
    extras=[
        snout((6, 8, 4), (4, 6, 3), 1, ".",
              faces={"front": ["gGGg", "gggg", "....", "mmmm", "....", "llll"],
                     "side": ["Ggg", "g.w", ".wk", "mm.", "...", "lll"],
                     "top": ["GgGg", "gGgG", "gggg"]}),
        Cube((-0.5, 8, -1), (1, 2, 3), "f",
             faces={"side": ["d..", "fd."], "front": ["d", "."]}),
    ] + pair(-4, 1, -1, (1, 2, 2), "f", faces={"side": ["f.", "dd"]}))


# --------------------------------------------------------------------------
# Sheep: a 6x6x2 face poking out of a fluffy 8x8x7 block of wool, as on the
# vanilla sheep (a 6x6 head inside an inflated wool layer). The wool colour
# follows the sheep's dye colour; the face stays the same.
# --------------------------------------------------------------------------
def wool(w, h, phase=0):
    """Fluffy wool tufts: a light top and a dark underside, offset per row."""
    rows = []
    for r in range(h):
        row = ""
        for c in range(w):
            k = (c + 2 * ((r + phase) // 2) + phase) % 4
            if (r + phase) % 2 == 0 and k == 0:
                row += "V"
            elif (r + phase) % 2 == 1 and k in (0, 1):
                row += "v"
            else:
                row += "."
        rows.append(row)
    return rows


SHEEP_WOOL = {
    "white": ("#e9ecec", "#c9cfcf", "#ffffff"),
    "orange": ("#f07613", "#c45d0d", "#f99a45"),
    "magenta": ("#bd44b3", "#952f8c", "#d672cd"),
    "light_blue": ("#3aafd9", "#2a8bb3", "#72cbeb"),
    "yellow": ("#f8c527", "#d6a312", "#fde06a"),
    "lime": ("#70b919", "#579112", "#94d646"),
    "pink": ("#ed8dac", "#d06e8e", "#f7b5ca"),
    "gray": ("#3e4447", "#2b3032", "#5a6266"),
    "light_gray": ("#8e8e86", "#6f6f68", "#acaca4"),
    "cyan": ("#158991", "#0e6a71", "#30a9b1"),
    "purple": ("#792aac", "#5d1f87", "#9549c8"),
    "blue": ("#35399d", "#26297b", "#5157c0"),
    "brown": ("#724728", "#57351c", "#8e5e3a"),
    "green": ("#546d1b", "#3f5313", "#6e8b2b"),
    "red": ("#a12722", "#7d1b17", "#c33f35"),
    "black": ("#1c1d21", "#0c0d0f", "#36383f"),
}


def sheep_variant(i, colour):
    base, dark, light = SHEEP_WOOL[colour]
    name = colour.replace("_", " ").title()
    return V(colour, f"{name} Sheep Head", {"color": i},
             pal={".": base, "v": dark, "V": light})


add("sheep", "Sheep Head", "Passive", size=(8, 8, 7),
    pal={".": SHEEP_WOOL["white"][0], "v": SHEEP_WOOL["white"][1],
         "V": SHEEP_WOOL["white"][2], "f": "#dcc1a2", "F": "#c3a482", "k": K, "w": W,
         "p": "#d08c86", "P": "#a86660"},
    front=wool(8, 8), side=wool(7, 8, 1), top=wool(8, 7, 2), back=wool(8, 8, 3),
    bottom=wool(8, 7, 1),
    extras=[snout((8, 8, 7), (6, 6, 2), 1, "f",
                  faces={"front": ["FFFFFF",
                                   "......",
                                   "wk..kw",
                                   "......",
                                   "F.pp.F",
                                   "..PP.."],
                         "side": ["FF", "..", "..", "..", "..", ".F"],
                         "top": ["FFFF.F", "F.FFFF"]})],
    variants=[sheep_variant(i, c) for i, c in enumerate(SHEEP_WOOL)])


# --------------------------------------------------------------------------
# Sniffer: the huge vanilla head (13x18x11 with a 13x14x9 snout and long
# ear flaps) scaled down to fit a block. Moss grows over the top.
# --------------------------------------------------------------------------
SNIFFER = (8, 10, 6)
add("sniffer", "Sniffer Head", "Passive", size=SNIFFER,
    pal={".": "#a8412f", "d": "#7a2a1e", "l": "#c45a40", "g": "#5f9c3a", "G": "#3f7428",
         "h": "#86c25a", "k": "#16241a", "e": "#3a8a6a", "n": "#c4583c", "N": "#8e3424",
         "o": "#e0806a", "t": "#ece0c8"},
    front=["gGgggGgg",
           "d......d",
           "........",
           "........",
           "........",
           "........",
           "........",
           "........",
           "........",
           "dddddddd"],
    side=["GgGhgG",
          "gGg.gg",
          "..d.ek",
          "....kk",
          "......",
          "......",
          "......",
          "......",
          "......",
          "dddddd"],
    top=["gGhgGghg",
         "GgGgGhgG",
         "ghgGgGgh",
         "gGgGhgGg",
         "hgGgGgGg",
         "gGgGgGhG"],
    back=["GgGhgGgG",
          "gGgggGhg",
          "g.gG.gg.",
          ".g...g..",
          "........",
          "d......d",
          "........",
          "........",
          "d......d",
          "dddddddd"],
    extras=[
        # Long lower beak, then the nose plate on top of it.
        snout(SNIFFER, (8, 7, 5), 1, "n",
              faces={"front": ["oooooooo",
                               "........",
                               "........",
                               "NNNNNNNN",
                               "NtNNNNtN",
                               "........",
                               "N......N"],
                     "side": ["ooooo", ".....", ".....", "NNNNN", "NNNNt", ".....", "NNNNN"],
                     "top": ["oooooooo"] * 5}),
        snout(SNIFFER, (8, 1, 5), 8, "G",
              faces={"front": ["gkGgGkgG"], "side": ["gGgGg"],
                     "top": ["GgGgGgGg", "gGhGgGhg", "GgGgGgGg", "gGgGgGgG", "GkgGgGkg"]}),
    ] + pair(-5, 0, -1, (1, 9, 4), "d",
             faces={"front": ["G", "g", ".", ".", ".", ".", ".", ".", "N"],
                    "side": ["gGgG", "GgGg", "..g.", "....", "....", "....",
                             "....", "....", "NNNN"],
                    "back": ["G", "g", ".", ".", ".", ".", ".", ".", "N"],
                    "top": ["g", "G", "g", "G"]}))


# --------------------------------------------------------------------------
# Snow golem: a carved pumpkin with its stem.
# --------------------------------------------------------------------------
PUMPKIN_SIDE = ["l.d..d.l",
                "l.d..d.l",
                "l.d..d.l",
                "l.d..d.l",
                "l.d..d.l",
                "l.d..d.l",
                "l.d..d.l",
                "d.d..d.d"]
add("snow_golem", "Snow Golem Head", "Passive",
    pal={".": "#e38a1d", "d": "#b8650f", "l": "#f2a43c", "k": "#2c1804", "K": "#4a2a08",
         "g": "#5e6e28", "G": "#3e4a18"},
    front=["l.d..d.l",
           "l.d..d.l",
           "lkK..Kkl",
           "lkk..kkl",
           "l.d..d.l",
           "lk.d..kl",
           "l.kkkk.l",
           "d.d..d.d"],
    side=PUMPKIN_SIDE,
    back=PUMPKIN_SIDE,
    top=["ld.ll.dl",
         "d.d..d.d",
         ".d.dd.d.",
         "l.dGGd.l",
         "l.dGGd.l",
         ".d.dd.d.",
         "d.d..d.d",
         "ld.ll.dl"],
    extras=[Cube((-1, 8, -1), (2, 2, 2), "g",
                 faces={"front": ["G.", ".G"], "side": [".G", "G."], "back": ["G.", ".G"],
                        "top": ["G.", "GG"]}),
            Cube((0, 10, -1), (1, 1, 1), "G")])


# --------------------------------------------------------------------------
# Squid: the whole squid body, with a ring of tentacle stubs round the base.
# --------------------------------------------------------------------------
SQUID_TENTACLE = {"front": ["d.", ".d", "l."], "side": ["d", ".", "l"],
                  "back": [".d", "d.", ".l"]}
SQUID_SIDE_TENTACLE = {"front": ["d", ".", "l"], "side": ["d.", ".d", "l."],
                       "back": ["d", ".", "l"]}
add("squid", "Squid Head", "Passive", size=(8, 10, 8),
    pal={".": "#2f4f72", "d": "#1e3550", "l": "#4a6c92", "w": "#dfe5ea", "k": K,
         "m": "#16243a", "t": "#3a5c82"},
    front=["dddddddd",
           "d.l..l.d",
           "........",
           ".d.l..d.",
           "........",
           "l......l",
           ".wk..kw.",
           ".ww..ww.",
           "...mm...",
           "d.d..d.d"],
    side=["dddddddd",
          "d.l..l.d",
          "........",
          ".l..d...",
          "......l.",
          "l.d.....",
          "........",
          "....l...",
          "........",
          "d.d..d.d"],
    top=["dddddddd",
         "d.l..l.d",
         "..d..d..",
         ".l.dd.l.",
         ".l.dd.l.",
         "..d..d..",
         "d.l..l.d",
         "dddddddd"],
    back=["dddddddd",
          "d.l..l.d",
          "........",
          "..d..l..",
          "........",
          "l......l",
          "..l..d..",
          "........",
          "........",
          "d.d..d.d"],
    extras=[Cube((-3, 0, -5), (2, 3, 1), "t", faces=SQUID_TENTACLE),
            Cube((1, 0, -5), (2, 3, 1), "t", faces=SQUID_TENTACLE),
            Cube((-3, 0, 4), (2, 3, 1), "t", faces=SQUID_TENTACLE),
            Cube((1, 0, 4), (2, 3, 1), "t", faces=SQUID_TENTACLE),
            Cube((-5, 0, -3), (1, 3, 2), "t", faces=SQUID_SIDE_TENTACLE),
            Cube((-5, 0, 1), (1, 3, 2), "t", faces=SQUID_SIDE_TENTACLE),
            Cube((4, 0, -3), (1, 3, 2), "t", faces=SQUID_SIDE_TENTACLE),
            Cube((4, 0, 1), (1, 3, 2), "t", faces=SQUID_SIDE_TENTACLE)])


# --------------------------------------------------------------------------
# Strider: its whole body, with the wiggly strands growing out of the top.
# --------------------------------------------------------------------------
def strider_strand(x, z, h, lean):
    """A strand leaning outwards: a straight base and a tip stepped sideways."""
    return [Cube((x, 8, z), (1, h, 1), "h", faces={"front": ["H"] + ["."] * (h - 1)}),
            Cube((x + lean, 8 + h, z), (1, 1, 1), "H")]


add("strider", "Strider Head", "Passive", size=(10, 8, 9),
    pal={".": "#a8302e", "d": "#7c1f20", "l": "#c44a42", "k": "#1c1214", "e": "#e8d0a0",
         "m": "#4a0e12", "t": "#e8dcc4", "h": "#6e5f73", "H": "#4c4054"},
    front=["dd.dddd.dd",
           "..l....l..",
           ".kk....kk.",
           ".ke....ek.",
           "..........",
           "mmmmmmmmmm",
           ".t.t..t.t.",
           "d.d.dd.d.d"],
    side=["dd.ddd.dd",
          "....l....",
          ".d.....d.",
          ".......kk",
          "...l.....",
          ".......mm",
          "d..d.....",
          "dd.d.d.dd"],
    top=["d.d.dd.d.d",
         ".l......l.",
         "..d.ll.d..",
         ".d......d.",
         "..l.dd.l..",
         ".d......d.",
         "..d.ll.d..",
         ".l......l.",
         "d.d.dd.d.d"],
    back=["dd.dddd.dd",
          "..l....l..",
          ".d..dd..d.",
          "..........",
          "...d..d...",
          "l........l",
          ".d..dd..d.",
          "d.d.dd.d.d"],
    extras=strider_strand(-4, -3.5, 3, -1) + strider_strand(3, -3.5, 3, 1)
    + strider_strand(-3, 0, 4, -1) + strider_strand(2, 0, 4, 1)
    + strider_strand(-4, 2.5, 2, -1) + strider_strand(3, 2.5, 2, 1))


# --------------------------------------------------------------------------
# Tadpole: the tiny 3x2x3 body scaled up twice, with a stub of tail.
# --------------------------------------------------------------------------
add("tadpole", "Tadpole Head", "Passive", size=(6, 4, 6),
    pal={".": "#4c3524", "d": "#36251a", "l": "#6e5038", "b": "#8a6a48", "k": "#0e0a08",
         "w": "#c8c0a8"},
    front=["d.dd.d",
           "kw..wk",
           "......",
           "bbbbbb"],
    side=["d.d..d",
          ".....k",
          "l..l..",
          "bbbbbb"],
    top=["d.dd.d",
         ".l..l.",
         "..dd..",
         ".l..l.",
         "k....k",
         "d.ll.d"],
    back=["d.dd.d",
          ".l..l.",
          "......",
          "bbbbbb"],
    extras=[Cube((-0.5, 0.5, 3), (1, 3, 4), "l",
                 faces={"side": ["l.d.", "d.l.", "l.d."], "back": ["d", ".", "d"]})])


# --------------------------------------------------------------------------
# Tropical fish: the front of the fish scaled up twice. Shape A (variant 0)
# is the small fish, shape B (variant 1) the tall one with a big top fin.
# Every pattern is painted over all the faces from one rule, so the markings
# wrap around the head.
# --------------------------------------------------------------------------
FISH_W, FISH_D = 4, 5


def fish_faces(h, rule):
    """Art for a fish body h pixels tall. rule(x, y, z, face) gives the pattern
    letter at a spot: x across (0..3), y down from the top, z back from the
    face (0 = front)."""
    W_, D_ = FISH_W, FISH_D
    front = [[rule(x, y, 0, "front") for x in range(W_)] for y in range(h)]
    side = [[rule(0, y, D_ - 1 - c, "side") for c in range(D_)] for y in range(h)]
    top = [[rule(x, 0, D_ - 1 - r, "top") for x in range(W_)] for r in range(D_)]
    back = [[rule(W_ - 1 - x, y, D_ - 1, "back") for x in range(W_)] for y in range(h)]
    side[2][3], side[2][4], side[1][3] = "k", "w", "w"
    front[h // 2][1] = front[h // 2][2] = "m"
    return {k: ["".join(r) for r in v]
            for k, v in (("front", front), ("side", side), ("top", top), ("back", back))}


def fish(shape, rule, base, base_dark, pat, pat_dark):
    h, fin_h, fin_d = (6, 2, 4) if shape == "a" else (8, 4, 5)
    fin_side = ["".join("q" if c % 2 == 0 else "." for c in range(fin_d))
                for r in range(fin_h)]
    return dict(
        size=(FISH_W, h, FISH_D),
        pal={".": base, "d": base_dark, "p": pat, "q": pat_dark},
        extras=[Cube((-0.5, h, -1.5 if fin_d == 4 else -2.5), (1, fin_h, fin_d), "p",
                     faces={"side": fin_side})],
        **fish_faces(h, rule))


def edge(x, y, z, face, h):
    """Base shading: darker along the top and bottom edges."""
    return "d" if y in (0, h - 1) else "."


FISH_PATTERNS = [
    # key, shape, mark rule, base, base shade, pattern, pattern shade
    ("kob", "a", lambda x, y, z, f, h: "p" if z in (2, 4) else "q" if z == 3 and y == 0 else
     edge(x, y, z, f, h), "#f07818", "#c85a0c", "#f4f0e8", "#2a2a2a"),
    ("sunstreak", "a", lambda x, y, z, f, h: "p" if y == 3 and (x in (0, 3) or z > 0) else
     "q" if y == 4 and z > 1 else edge(x, y, z, f, h), "#b8221c", "#86160f", "#f4f0e8",
     "#d8d0c4"),
    ("snooper", "a", lambda x, y, z, f, h: "p" if y <= 1 and z <= 2 else
     "q" if y == 2 and z <= 1 else edge(x, y, z, f, h), "#8a8a8a", "#686868", "#c8261e",
     "#8e1812"),
    ("dasher", "a", lambda x, y, z, f, h: "p" if y <= 1 and (z + y) % 2 == 0 and x in (1, 2)
     or (f == "side" and y == 1 and z % 2 == 0) else edge(x, y, z, f, h),
     "#2ab8c0", "#1a8890", "#f08aaa", "#c8607e"),
    ("brinely", "a", lambda x, y, z, f, h: "p" if y >= 3 else "q" if y == 2 and z % 2 == 1
     else edge(x, y, z, f, h), "#7ccc2a", "#5a9e18", "#8ac8f0", "#5a9ad0"),
    ("spotty", "a", lambda x, y, z, f, h: "p" if (x * 2 + y * 3 + z * 2) % 5 == 0 else
     edge(x, y, z, f, h), "#f2efe6", "#cfc8b8", "#f4d22a", "#c8a414"),
    ("flopper", "b", lambda x, y, z, f, h: "p" if y <= 1 or y >= h - 2 else
     "q" if y in (2, h - 3) and z % 2 == 0 else ".", "#f2efe6", "#cfc8b8", "#f4d22a",
     "#c8a414"),
    ("stripey", "b", lambda x, y, z, f, h: "p" if y % 2 == 1 else edge(x, y, z, f, h),
     "#f2c81e", "#c89e0e", "#6e6a62", "#4a4740"),
    ("glitter", "b", lambda x, y, z, f, h: "p" if (y * 5 + z * 3 + x) % 4 == 1 else
     "q" if (y * 5 + z * 3 + x) % 7 == 3 else edge(x, y, z, f, h), "#f2efe6", "#cfc8b8",
     "#8c8c8c", "#5e5e5e"),
    ("blockfish", "b", lambda x, y, z, f, h: "p" if 2 <= y <= 5 and 1 <= z <= 3 and
     (f != "front" and f != "back" or x in (1, 2)) else edge(x, y, z, f, h),
     "#b8221c", "#86160f", "#f4f0e8", "#d8d0c4"),
    ("betty", "b", lambda x, y, z, f, h: "p" if z % 2 == 1 and y not in (0, h - 1) else
     edge(x, y, z, f, h), "#c8281e", "#901a12", "#f4f0e8", "#d8d0c4"),
    ("clayfish", "b", lambda x, y, z, f, h: "p" if y >= h - 3 or (y <= 1 and z >= 2) else
     "q" if y == h - 4 and z % 2 == 0 else ".", "#f2efe6", "#cfc8b8", "#ec8a32",
     "#c06418"),
]


def fish_variant(key, shape, rule, *colours):
    h = 6 if shape == "a" else 8
    match = {"variant": 0 if shape == "a" else 1,
             "mark_variant": [p[0] for p in FISH_PATTERNS if p[1] == shape].index(key)}
    return V(key, f"{key.title()} Tropical Fish Head", match,
             **fish(shape, lambda x, y, z, f: rule(x, y, z, f, h), *colours))


FISH_VARIANTS = [fish_variant(*p) for p in FISH_PATTERNS]
FISH_DEFAULT = dict(FISH_VARIANTS[0].changes)
add("tropicalfish", "Tropical Fish Head", "Passive",
    **{**FISH_DEFAULT, "pal": {"k": K, "w": W, "m": "#3a1a10", **FISH_DEFAULT["pal"]}},
    variants=FISH_VARIANTS)


# --------------------------------------------------------------------------
# Turtle: vanilla 6x5x6 head, green and speckled with a pale chin.
# --------------------------------------------------------------------------
add("turtle", "Turtle Head", "Passive", size=(6, 5, 6),
    pal={".": "#4fa04a", "d": "#3a7d36", "D": "#2a5c27", "l": "#7ec06a", "y": "#d4e2a2",
         "Y": "#b0c47c", "k": K, "m": "#24401f"},
    front=["d.Dd.d",
           ".l..l.",
           "k....k",
           "l.mm.l",
           "yyyyyy"],
    side=["D.d.D.",
          ".d..l.",
          "d.D..k",
          ".l..ll",
          "YyyYyy"],
    top=["D.d.D.",
         ".d.D.d",
         "d.D.d.",
         ".D.d.D",
         "d.l.d.",
         ".l.l.l"],
    back=["d.D.d.",
          ".D.d.D",
          "d.d.D.",
          ".l.d.l",
          "YyyyyY"])


# --------------------------------------------------------------------------
# Villagers: the 8x10x8 head with its 2x4x2 nose, unibrow and green eyes.
# Biome variants wear their own headband or hat.
# --------------------------------------------------------------------------
VILLAGER = (8, 10, 8)
VILLAGER_NOSE = snout(VILLAGER, (2, 4, 2), 0, "n",
                      faces={"front": ["..", "..", "..", "NN"], "side": ["..", "..", ".N", "NN"],
                             "top": ["N.", ".."]})
VILLAGER_PAL = {".": "#bd8b72", "s": "#a6765e", "S": "#8e624c", "l": "#cc9b82",
                "b": "#3d2a1f", "w": W, "g": "#2b8a3b", "n": "#b07c62", "N": "#946450"}
VILLAGER_ART = dict(
    front=["........",
           "l......l",
           "........",
           ".bbbbbb.",
           ".wg..gw.",
           "........",
           "s......s",
           "........",
           "s......s",
           "ss....ss"],
    side=["s.......",
          "........",
          ".....l..",
          "s.......",
          "........",
          "........",
          "s.......",
          "s.......",
          "ss......",
          "Sss...ss"],
    top=["s......s",
         "...l....",
         "..l.l...",
         "........",
         "....l...",
         "........",
         "........",
         "s......s"],
    back=["........",
          "...l....",
          "........",
          "s......s",
          "........",
          "........",
          "s......s",
          "s......s",
          "ss....ss",
          "SssssssS"],
)


def villager_band(row1, row2, side1, side2, back1=None, back2=None):
    """Villager art with a headband painted over rows 1 and 2."""
    a = VILLAGER_ART
    return dict(front=paint(a["front"], {1: row1, 2: row2}),
                side=paint(a["side"], {1: side1, 2: side2}),
                back=paint(a["back"], {1: back1 or side1, 2: back2 or side2}),
                top=a["top"])


def villager_hat(colour, shade):
    """Villager art for a brimmed hat: the top row of the head is the hat."""
    a = VILLAGER_ART
    return dict(front=paint(a["front"], {0: colour * 8, 1: shade * 8}),
                side=paint(a["side"], {0: colour * 8, 1: shade * 8}),
                back=paint(a["back"], {0: colour * 8, 1: shade * 8}),
                top=a["top"])


VILLAGER_DESERT = villager_band("hhhrrhhh", "HHHRRHHH", "hhhhhhhh", "HHHHHHHH")
VILLAGER_JUNGLE = dict(
    villager_band("jJjyjjJj", "JjJJjJjJ", "jJjjJjjJ", "JjJJjJJj"),
    extras=[VILLAGER_NOSE]
    + pair(-3.5, 9, -4.5, (2, 2, 1), "j", faces={"front": ["J.", "jJ"], "top": ["J."]})
    + pair(-4.5, 9, -1, (1, 2, 2), "j", faces={"side": [".J", "Jj"], "top": ["J", "."]})
    + [Cube((-1, 9, 3.5), (2, 2, 1), "j", faces={"back": [".J", "Jj"]}),
       Cube((-0.5, 10, -4.5), (1, 1, 1), "y")])
VILLAGER_SAVANNA = villager_band("aaaaaaaa", "ayAyyAya", "aaaaaaaa", "AyAyAyAy")
VILLAGER_SNOW = dict(
    VILLAGER_ART,
    extras=[VILLAGER_NOSE,
            Cube((-4.5, 7, -4.5), (9, 4, 9), "c",
                 faces={"front": ["cCcfcCcfc", "fcCcfcCcf", "cfcCcfcCc", "TtTtTtTtT"],
                        "side": ["cCcfcCcfc", "fcCcfcCcf", "cfcCcfcCc", "TtTtTtTtT"],
                        "back": ["cCcfcCcfc", "fcCcfcCcf", "cfcCcfcCc", "TtTtTtTtT"],
                        "top": ["fcCcfcCcf", "cCcfcCcfc", "fcfcCcfcf", "cCcfcfcCc",
                                "fcCcTcCcf", "cCcfcfcCc", "fcfcCcfcf", "cCcfcCcfc",
                                "fcCcfcCcf"]})]
    + pair(-4.5, 4, -2.5, (1, 3, 4), "c",
           faces={"front": ["c", "C", "T"], "side": ["cfcC", "CcCf", "TtTt"],
                  "back": ["c", "C", "T"]}))
VILLAGER_SWAMP = dict(
    villager_hat("q", "Q"),
    extras=[VILLAGER_NOSE,
            Cube((-5, 8, -5), (10, 1, 10), "q",
                 faces={"front": ["QqQqQQqQqQ"], "side": ["qQqQqqQqQq"],
                        "back": ["QqQqQQqQqQ"],
                        "top": ["QqvqQqQvqQ", "q........q", "v........Q", "Q........q",
                                "q........v", "Q........Q", "q........q", "v........Q",
                                "Q........q", "qQqvQqQqvQ"]}),
            Cube((-4, 10, -4), (8, 2, 8), "q",
                 faces={"front": ["qvqQqvQq", "QqQqQqQq"], "side": ["qQvqQqvQ", "QqQqQqQq"],
                        "back": ["qvqQqvQq", "QqQqQqQq"],
                        "top": ["qQvqQqvQ", "Qq.qQ.qq", "vqQqvqQq", "qQqLqQvq",
                                "QqvqQqLq", "q.qQvq.Q", "QvqQqQqv", "qQqvqQqQ"]}),
            Cube((-1, 12, -1), (2, 1, 2), "L", faces={"front": ["v."], "side": [".v"]})]
    + pair(-5, 5, -5, (1, 3, 1), "v", faces={"front": ["Q", "v", "q"], "side": ["Q", "v", "q"]}))
VILLAGER_TAIGA = dict(
    villager_hat("t", "T"),
    extras=[VILLAGER_NOSE,
            Cube((-5, 8, -5), (10, 1, 10), "t",
                 faces={"front": ["TTTTTTTTTT"], "side": ["TTTTTTTTTT"], "back": ["TTTTTTTTTT"],
                        "top": ["tutttttutt", "u........t", "t........t", "t........u",
                                "t........t", "u........t", "t........t", "t........u",
                                "t........t", "ttutttuttt"]}),
            Cube((-4, 10, -4), (8, 3, 8), "t",
                 faces={"front": ["tuttuttu", "tttttttt", "FfFfFfFf"],
                        "side": ["ttuttutt", "tttttttt", "fFfFfFfF"],
                        "back": ["tuttuttu", "tttttttt", "FfFfFfFf"],
                        "top": ["tttutttt", "t.....ut", "t.u....t", "u......t",
                                "t......u", "t....u.t", "tu.....t", "ttttuttt"]})])
VILLAGER_HAT_PAL = {
    "h": "#e0a832", "H": "#b07a1c", "r": "#c0281e", "R": "#8a1a12",
    "j": "#3f8f2a", "J": "#2a6a1c", "y": "#f0d040",
    "a": "#c8482a", "A": "#e07a2a",
    "c": "#ece8e0", "C": "#cfc8bc", "f": "#ffffff", "T": "#8a8478", "t": "#a8a294",
    "q": "#4e6a2c", "Q": "#3a5020", "v": "#6a8a3a", "L": "#86a84a",
}

add("villager", "Villager Head", "Passive", ["minecraft:villager_v2", "minecraft:villager"],
    size=VILLAGER, pal={**VILLAGER_PAL, **VILLAGER_HAT_PAL, "u": "#5a3e26", "F": "#8a6a44", "f": "#a8865a"},
    **VILLAGER_ART,
    extras=[VILLAGER_NOSE],
    variants=[
        V("plains", "Plains Villager Head", {"mark_variant": 0}),
        V("desert", "Desert Villager Head", {"mark_variant": 1}, **VILLAGER_DESERT),
        V("jungle", "Jungle Villager Head", {"mark_variant": 2}, **VILLAGER_JUNGLE),
        V("savanna", "Savanna Villager Head", {"mark_variant": 3}, **VILLAGER_SAVANNA),
        V("snow", "Snowy Villager Head", {"mark_variant": 4},
          pal={"f": "#ffffff"}, **VILLAGER_SNOW),
        V("swamp", "Swamp Villager Head", {"mark_variant": 5}, **VILLAGER_SWAMP),
        V("taiga", "Taiga Villager Head", {"mark_variant": 6},
          pal={"t": "#6b4a2e", "T": "#4f3520"}, **VILLAGER_TAIGA),
    ])

# The wandering trader wears a blue hood: a cube set half a pixel behind the
# face, so it frames the face and covers the rest of the head.
add("wandering_trader", "Wandering Trader Head", "Passive", size=VILLAGER,
    pal={**VILLAGER_PAL, "h": "#3a56a8", "H": "#2a3f80", "i": "#5874c6", "y": "#c9a64a"},
    **VILLAGER_ART,
    extras=[VILLAGER_NOSE,
            Cube((-5, 0.5, -3.5), (10, 11, 8), "h",
                 faces={"front": ["iiiiiiiiii"] + ["i........i"] * 9 + ["iH......Hi"],
                        "side": ["HhhhhhhH", "hhihhhhh", "Hhhhihhh", "hHhhhhih",
                                 "hhhHhhhh", "hhHhhhhh", "hhhhhHhh", "Hhhhhhhh",
                                 "hhHhhhhh", "hHhhhhHh", "HHHHHHHH"],
                        "back": ["HhhhhhhhhH", "hhhhiihhhh", "hhhiHHihhh", "hhhHhhHhhh",
                                 "hhHhhhhHhh", "hhhhhhhhhh", "hHhhhhhhHh", "hhhhhhhhhh",
                                 "Hhhhhhhhhh", "hhhhhhhhhH", "HHHHHHHHHH"],
                        "top": ["HhhhhhhhhH", "hhhiihhhhh", "hhhhhhihhh", "hhihhhhhhh",
                                "hhhhhhhhih", "hhhhihhhhh", "hihhhhhhhh", "iiiiiiiiii"]})])


# --------------------------------------------------------------------------
# Sulfur cube: a chunky block of sulfur crystal with a face.
# --------------------------------------------------------------------------
SULFUR_SIDE = ["dddddddddd",
               "d.l...l..d",
               "dl..d...ld",
               "d..ddd...d",
               "d...d..l.d",
               "d.l....ldd",
               "d..l.d...d",
               "d.....ddld",
               "dl.l.....d",
               "dddddddddd"]
add("sulfur_cube", "Sulfur Cube Head", "Passive", size=(10, 10, 10),
    pal={".": "#d4d240", "d": "#a09e24", "l": "#eeec8a", "o": "#7e7c18", "k": "#2c2e0e",
         "e": "#f8f6c0"},
    front=["dddddddddd",
           "d.l....l.d",
           "dl......ld",
           "d.kk..kk.d",
           "d.ke..ke.d",
           "d........d",
           "d..l..l..d",
           "d...kk...d",
           "dl......ld",
           "dddddddddd"],
    side=SULFUR_SIDE,
    back=SULFUR_SIDE,
    top=["dddddddddd",
         "d.l..l...d",
         "dl.dd..l.d",
         "d..d.l...d",
         "d.l...dd.d",
         "d..l..d..d",
         "d.dd....ld",
         "d...l.d..d",
         "dl.....l.d",
         "dddddddddd"],
    experimental=True)
