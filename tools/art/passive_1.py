"""Head art: Passive mobs, part 1 (allay to horse).

See tools/mobs.py for the coordinate system and the art conventions.
Reminder: on the front and top, the LEFT column of the art is the +x (east)
side of the mob; on the back the left column is -x (west). pair() takes the
-x cube's art and mirrors it for the +x cube.
"""

from mobs import K, W, Cube, V, add, pair, snout, solid  # noqa: F401


# --------------------------------------------------------------------------
# Allay: vanilla 5x5x5 head, drawn at 6x6x6 to give the eyes room.
# --------------------------------------------------------------------------
add("allay", "Allay Head", "Passive", size=(6, 6, 6),
    pal={".": "#5fcbf2", "l": "#9be6ff", "L": "#d4f6ff", "d": "#3fa6dc", "D": "#2a7cbc",
         "b": "#3d5fd0", "k": "#16267a"},
    front=["LlLLlL",
           "l....l",
           ".b..b.",
           ".k..k.",
           "d....d",
           "Dd..dD"],
    side=["LLlLll",
          "l.l...",
          "......",
          "d.....",
          "dd....",
          "DDd..d"],
    top=["llllll",
         "lLllll",
         "llllLl",
         "l.llll",
         "lllL.l",
         "LlLLlL"],
    back=["lLllLl",
          "l....l",
          "..l...",
          "d....d",
          "dd..dd",
          "DDddDD"],
    bottom_fill="d")

# --------------------------------------------------------------------------
# Armadillo: vanilla head is a small 3x5x2 snout tipped forward with two tall
# ears. Scaled up to a 4x6x4 head with a nose tip and leaf-shaped ears.
# --------------------------------------------------------------------------
ARMADILLO = (4, 6, 4)
add("armadillo", "Armadillo Head", "Passive", size=ARMADILLO,
    pal={".": "#b97e70", "d": "#8a5448", "l": "#dba696", "k": "#1a1010",
         "n": "#6d3a34", "e": "#a86a5c", "i": "#e8ae9f"},
    front=["d..d",
           "l..l",
           "k..k",
           "....",
           ".ll.",
           "dlld"],
    side=["dd.d",
          "d..l",
          "d..k",
          "d...",
          "dd.l",
          "ddll"],
    top=["dddd",
         "d..d",
         "....",
         "l..l"],
    back=["dddd",
          "dddd",
          "d..d",
          "....",
          "d..d",
          "dddd"],
    bottom_fill="l",
    extras=[snout(ARMADILLO, (2, 2, 1), 0, "n", faces={"front": ["kk", "nn"]})]
    + pair(-4, 4, -0.5, (2, 4, 1), "e",
           faces={"front": ["e.", "ii", "ii", "ie"], "back": [".e", "ee", "ee", "e."],
                  "top": ["ee"]}))

# --------------------------------------------------------------------------
# Axolotl: 8x5x5 head, frilly gills on both sides and on top.
# "s" are speckles (bold on the wild axolotl, faint on the others).
# --------------------------------------------------------------------------
AXOLOTL = (8, 5, 5)
AX_SIDE_GILL = {"front": ["tt.", "..G", "tt.", "..G", "tt.", "..G", "..G"],
                "back": [".tt", "G..", ".tt", "G..", ".tt", "G..", "G.."],
                "side": ["t", ".", "t", ".", "t", ".", "G"],
                "top": ["tt."]}
AX_TOP_GILL = {"front": ["t.t..t.t", ".G.tt.G.", "G..GG..G"],
               "back": ["t.t..t.t", ".G.tt.G.", "G..GG..G"],
               "side": ["t", ".", "G"],
               "top": ["t.t..t.t"]}


def axolotl_pal(base, shade, light, spots, eye, mouth, gill, gill_dark, gill_tip):
    return {".": base, "d": shade, "l": light, "s": spots, "k": eye, "m": mouth,
            "g": gill, "G": gill_dark, "t": gill_tip}


add("axolotl", "Axolotl Head", "Passive", size=AXOLOTL,
    pal=axolotl_pal("#f7a8c8", "#e88db2", "#fcd6e4", "#ef9bbd", "#2a1520", "#b8507c",
                    "#d9467f", "#a8305f", "#f37aa8"),
    front=["d.s..s.d",
           "k......k",
           "........",
           "..mmmm..",
           "dlllllld"],
    side=["s.s..",
          "..s.k",
          "s....",
          ".s...",
          "dllll"],
    top=["d.s..s.d",
         "..s..s..",
         ".s....s.",
         "...ss...",
         "s......s"],
    back=["d.s..s.d",
          "..s.s...",
          "s....s..",
          "...s...s",
          "dlllllld"],
    bottom_fill="l",
    extras=pair(-7, 0, 0.5, (3, 7, 1), "g", faces=AX_SIDE_GILL)
    + [Cube((-4, 5, 0.5), (8, 3, 1), "g", faces=AX_TOP_GILL)],
    variants=[
        V("lucy", "Lucy Axolotl Head", {"variant": 0}),
        V("wild", "Wild Axolotl Head", {"variant": 3},
          pal=axolotl_pal("#7c5a3c", "#5e4430", "#a68866", "#3e2a1c", "#140d08", "#2e2016",
                          "#8a5a46", "#5e3a2c", "#c48e72")),
        V("gold", "Gold Axolotl Head", {"variant": 2},
          pal=axolotl_pal("#f4c443", "#dca52c", "#fde68e", "#e6b032", "#3a2a10", "#a87012",
                          "#e89a22", "#bd7612", "#ffd860")),
        V("cyan", "Cyan Axolotl Head", {"variant": 1},
          pal=axolotl_pal("#cdeef2", "#a8d6de", "#effbfc", "#b6e0e8", "#2a3a6a", "#6f9cac",
                          "#e07ab8", "#b45a96", "#f6b0dc")),
        V("blue", "Blue Axolotl Head", {"variant": 4},
          pal=axolotl_pal("#5265d8", "#3d4cb2", "#8494f0", "#33409a", "#0e1440", "#222c78",
                          "#36449e", "#25307a", "#8fa0f4")),
    ])

# --------------------------------------------------------------------------
# Bat: vanilla head is a tiny 4x3x2 with big 3x5 ears. Scaled up ~1.5x.
# --------------------------------------------------------------------------
add("bat", "Bat Head", "Passive", size=(6, 5, 4),
    pal={".": "#4a3828", "d": "#2f2219", "l": "#6e5240", "k": "#0c0c0c", "n": "#24180f",
         "w": "#ece4d4", "p": "#8a5c4e"},
    front=["d....d",
           ".k..k.",
           ".llll.",
           "dlnnld",
           "dwddwd"],
    side=["dd..",
          "d...",
          "d..l",
          "dd.l",
          "dddd"],
    top=["d.dd.d",
         "......",
         "..ll..",
         "l....l"],
    back=["d....d",
          "..dd..",
          "......",
          "d....d",
          "dddddd"],
    bottom_fill="d",
    extras=pair(-5, 5, 0, (3, 5, 1), "d",
                faces={"front": ["d..", "dpd", ".pd", ".pp", "..."],
                       "back": ["..d", "d.d", "d..", "...", "d.."],
                       "side": ["d", ".", ".", ".", "."]}))

# --------------------------------------------------------------------------
# Camel: the top of the long neck (7x7x7) with the 5x5x6 head sticking out
# forward at the top, and two sideways ears.
# --------------------------------------------------------------------------
CAMEL = (7, 7, 6)
add("camel", "Camel Head", "Passive", size=CAMEL,
    pal={".": "#d8a860", "d": "#bb8a4a", "D": "#9a6e38", "l": "#ecc88a", "k": "#1e140c",
         "n": "#5a3a20", "m": "#7a5030"},
    front=["d.....d",
           "d.....d",
           "d.....d",
           "......d",
           "d......",
           "d.lll.d",
           "dllllld"],
    side=["Dd....",
          "d.....",
          "d..d..",
          "d.....",
          "....d.",
          "d..l..",
          "dd.lll"],
    top=["DdddddD",
         "d.....d",
         "..d.d..",
         ".d...d.",
         "d.....d",
         "......."],
    back=["DdddddD",
          "d.....d",
          "..d.d..",
          "..ddd..",
          ".......",
          "d.....d",
          "ddddddd"],
    bottom_fill="d",
    extras=[snout(CAMEL, (5, 5, 5), 2, ".",
                  faces={"front": ["d...d", "n...n", "..d..", "lmmml", "lllll"],
                         "side": ["dD...", ".k...", "d....", "lll.m", "lllll"],
                         "top": ["ddddd", "d...d", ".....", "..d..", "....."],
                         "bottom": solid(5, 5, "l")})]
    + pair(-6.5, 5.5, 0.5, (3, 1, 2), "d",
           faces={"front": ["Dd."], "back": [".dD"], "top": ["Dd.", "Dd."]}))

# --------------------------------------------------------------------------
# Cat: vanilla 5x4x5 head with a 3x2 nose and 1x1x2 ears, drawn at 7x6x7.
# One set of art with colour classes; each breed only changes the palette:
#   s stripes, a / b patches (calico orange / black), M face mask,
#   m muzzle and cheeks, c chin, e / f east / west ear, i inner ear.
# --------------------------------------------------------------------------
CAT = (7, 6, 7)
CAT_FRONT = ["asas.s.",
             "aaMMM..",
             "agkMkg.",
             "amMMMm.",
             "mm...mm",
             "cc...cc"]
CAT_SIDE_E = ["s.s.saa",
              ".s.s.aa",
              "s.s.s.a",
              ".s.s..a",
              "s...mmm",
              "..ccccc"]
CAT_SIDE_W = ["bbbs.s.",
              "bbs.s..",
              "bs.s.s.",
              ".s.s...",
              "s...mmm",
              "..ccccc"]
CAT_TOP = ["..sbbbb",
           "..s.bbb",
           "..s.sbb",
           "aas.s..",
           "aaa.s..",
           "aas.s..",
           "asas.s."]
CAT_BACK = ["bbbbs..",
            "bbbs.s.",
            "bb.s.s.",
            "b.s.s.s",
            ".s.s.s.",
            "......."]
CAT_NOSE = Cube((-1.5, 0, -4.5), (3, 2, 1), "m",
                faces={"front": ["MnM", "mmm"], "top": ["MMM"], "side": ["M", "m"]})
CAT_EARS = [Cube((1.5, 6, 0.5), (2, 2, 2), "e",
                 faces={"front": ["ee", "ei"], "top": ["ee", "ee"]}),
            Cube((-3.5, 6, 0.5), (2, 2, 2), "f",
                 faces={"front": ["ff", "if"], "top": ["ff", "ff"]})]


def cat_pal(base, stripe=None, muzzle=None, chin=None, mask=None, a=None, b=None,
            ear=None, ear_w=None, inner="#d89a9a", nose="#d88c8c", iris="#7cc243",
            pupil="#101010"):
    return {".": base, "s": stripe or base, "m": muzzle or base, "c": chin or muzzle or base,
            "M": mask or base, "a": a or base, "b": b or base, "e": ear or base,
            "f": ear_w or ear or base, "i": inner, "n": nose, "g": iris, "k": pupil}


add("cat", "Cat Head", "Passive", size=CAT,
    pal=cat_pal("#8e6c4a", stripe="#4e3a28", muzzle="#c8a882", chin="#e0cdb0"),
    front=CAT_FRONT, side=CAT_SIDE_E, west=CAT_SIDE_W, top=CAT_TOP, back=CAT_BACK,
    bottom_fill="c",
    extras=[CAT_NOSE] + CAT_EARS,
    variants=[
        V("tabby", "Tabby Cat Head", {"variant": 8}),
        V("tuxedo", "Tuxedo Cat Head", {"variant": 1},
          pal=cat_pal("#1d1d24", stripe="#272730", muzzle="#ececec", chin="#f6f6f6",
                      inner="#6a4a50", nose="#c88a8a", iris="#6fc04a", pupil="#050505")),
        V("red", "Red Cat Head", {"variant": 2},
          pal=cat_pal("#e2913a", stripe="#b2601c", muzzle="#f2c48a", chin="#f8dcb0",
                      inner="#f0a8a0", nose="#e09a9a", iris="#b8d030")),
        V("siamese", "Siamese Cat Head", {"variant": 3},
          pal=cat_pal("#efe2c6", stripe="#e6d6b6", muzzle="#4a3426", chin="#5c4434",
                      mask="#4a3426", ear="#4a3426", inner="#6a4a3a", nose="#24180f",
                      iris="#5ab0e8")),
        V("british_shorthair", "British Shorthair Cat Head", {"variant": 4},
          pal=cat_pal("#8a9098", stripe="#767c86", muzzle="#a2a8b0", chin="#b0b6be",
                      inner="#a08890", nose="#5a5a64", iris="#e0b030")),
        V("calico", "Calico Cat Head", {"variant": 5},
          pal=cat_pal("#f2ece2", stripe="#f2ece2", muzzle="#faf6f0", chin="#ffffff",
                      a="#e08a32", b="#2a2420", ear="#e08a32", ear_w="#2a2420",
                      inner="#e8a0a0", nose="#e8a0a0", iris="#9ac040")),
        V("persian", "Persian Cat Head", {"variant": 6},
          pal=cat_pal("#ecc890", stripe="#ddb47a", muzzle="#f8e4c0", chin="#fff2dc",
                      inner="#f0b0a0", nose="#e8a0a0", iris="#d8a838")),
        V("ragdoll", "Ragdoll Cat Head", {"variant": 7},
          pal=cat_pal("#efe6d6", stripe="#e6dac6", muzzle="#fbf8f2", chin="#ffffff",
                      mask="#7a5a44", ear="#6a4a38", inner="#8a6a58", nose="#d89a9a",
                      iris="#5a9ee8")),
        V("white", "White Cat Head", {"variant": 0},
          pal=cat_pal("#f2f2f2", stripe="#e2e2e8", muzzle="#ffffff", chin="#ffffff",
                      inner="#f0b8c0", nose="#f0a8b0", iris="#5ab0e0")),
        V("jellie", "Jellie Cat Head", {"variant": 10},
          pal=cat_pal("#3a3a42", stripe="#2a2a30", muzzle="#ececec", chin="#f6f6f6",
                      a="#9a9aa4", inner="#7a6a70", nose="#d08a8a", iris="#a8c838")),
        V("black", "Black Cat Head", {"variant": 9},
          pal=cat_pal("#1a1a20", stripe="#24242c", muzzle="#26262e", chin="#2c2c34",
                      inner="#3a2a30", nose="#3a3a44", iris="#c8d838", pupil="#050505")),
    ])

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

# --------------------------------------------------------------------------
# Cod: vanilla head is 2x4x3 plus a 2x3x1 nose. Scaled up 2x.
# --------------------------------------------------------------------------
COD = (4, 8, 6)
add("cod", "Cod Head", "Passive", size=COD,
    pal={".": "#b39c74", "d": "#8e7754", "D": "#6e5a3c", "l": "#d8c8a4", "L": "#ece2cc",
         "s": "#9c8460", "k": "#101010", "w": "#e8e0d0", "m": "#4e3e2a", "r": "#7a5a40"},
    front=["DDDD",
           "dddd",
           "d..d",
           "....",
           "....",
           "....",
           "llll",
           "LLLL"],
    side=["DdDDdD",
          "rd.sd.",
          "r..ww.",
          "r.swk.",
          "r...s.",
          "l.l...",
          "llllll",
          "LLLLLL"],
    top=["DDDD",
         "DsDD",
         "DDsD",
         "DsDD",
         "DDDD",
         "dDDd"],
    back=["DDDD",
          "dddd",
          "d..d",
          "....",
          "s..s",
          "l..l",
          "llll",
          "LLLL"],
    bottom_fill="L",
    extras=[snout(COD, (4, 6, 2), 2, ".",
                  faces={"front": ["dDDd", "d..d", "....", "mmmm", "llll", "LLLL"],
                         "side": ["dd", "d.", "..", "mm", "ll", "LL"],
                         "top": ["DDDD", "dDDd"],
                         "bottom": solid(4, 2, "L")})])

# --------------------------------------------------------------------------
# Copper golem: 8x5x10 head, long nose, lightning-rod antenna with a knob.
# "p" is the oxidation patch colour; each stage recolours the same art.
# --------------------------------------------------------------------------
COPPER = (8, 5, 10)


def copper_pal(base, light, lighter, dark, darker, patch):
    return {".": base, "l": light, "L": lighter, "d": dark, "D": darker, "p": patch,
            "k": "#1c2a30"}


add("copper_golem", "Copper Golem Head", "Passive", size=COPPER,
    pal=copper_pal("#c86f4a", "#e08a5e", "#f4ac7c", "#a0503a", "#7a3a28", "#b25e40"),
    front=["lLlpllLl",
           "..p.....",
           ".kk..kk.",
           ".kk..kk.",
           "d.....pd"],
    side=["llLlllpllL",
          "..........",
          ".p....d...",
          "......d..p",
          "dddpdddddd"],
    top=["lllLllll",
         "l.p....l",
         "........",
         "...p....",
         "........",
         "........",
         ".p......",
         "......p.",
         "l......l",
         "lLlpllLl"],
    back=["llLllpll",
          "..p.....",
          ".....p..",
          "........",
          "dddddddd"],
    bottom_fill="d",
    extras=[Cube((-1, 0, -6), (2, 3, 2), ".",
                 faces={"front": ["ll", "..", "dd"], "side": ["ll", "..", "dd"],
                        "top": ["LL", "ll"]}),
            Cube((-1, 5, -1), (2, 4, 2), "d",
                 faces={"front": ["l.", "l.", "lp", "l."], "side": ["l.", "lp", "l.", "l."],
                        "back": [".D", "pD", ".D", ".D"]}),
            Cube((-2, 9, -2), (4, 4, 4), ".",
                 faces={"front": ["LLl.", "L..p", "...d", ".pdd"],
                        "side": ["lLl.", "l...", "..pd", ".ddd"],
                        "back": [".llL", "p..l", "d...", "dd.p"],
                        "top": ["lLLl", "LLll", "lLlp", "llld"]})],
    variants=[
        V("unoxidized", "Copper Golem Head", {"minecraft:oxidation_level": "unoxidized"}),
        V("exposed", "Exposed Copper Golem Head", {"minecraft:oxidation_level": "exposed"},
          pal=copper_pal("#a87c64", "#c0927a", "#d4aa8e", "#7e5c4a", "#5e4436", "#7fa086")),
        V("weathered", "Weathered Copper Golem Head",
          {"minecraft:oxidation_level": "weathered"},
          pal=copper_pal("#64a283", "#7cbc98", "#9ad2b2", "#4a7e66", "#36604c", "#a07a58")),
        V("oxidized", "Oxidized Copper Golem Head", {"minecraft:oxidation_level": "oxidized"},
          pal=copper_pal("#4fa58c", "#68c0a4", "#8ad8bc", "#3a806a", "#2a6050", "#3a8a74")),
    ])

# --------------------------------------------------------------------------
# Cow: 8x8x6 head with a 6x3x1 muzzle. Temperate cows have small horns,
# warm cows wide horns that turn upwards, cold cows shaggy fur and horns
# pointing forwards.
# --------------------------------------------------------------------------
COW = (8, 8, 6)
COW_MUZZLE = snout(COW, (6, 3, 1), 0, "m",
                   faces={"front": ["mmmmmm", "mnmmnm", "MMMMMM"], "top": ["mmmmmm"],
                          "side": ["m", "m", "M"]})
COW_HORNS = pair(-5, 6, -2, (1, 3, 1), "h",
                 faces={"front": ["H", "h", "h"], "side": ["H", "h", "h"],
                        "back": ["H", "h", "h"]})
WARM_HORNS = (pair(-8, 5, -2, (4, 2, 2), "h",
                   faces={"front": ["hhhh", "ghhh"], "back": ["hhhh", "hhhg"],
                          "side": ["hh", "gg"], "top": ["hhhh", "hhhh"]})
              + pair(-8, 7, -2, (2, 2, 2), "h",
                     faces={"front": ["HH", "hh"], "back": ["HH", "hh"],
                            "side": ["HH", "hh"], "top": ["HH", "HH"]}))
COLD_HORNS = pair(-6, 5, -4, (2, 2, 5), "h",
                  faces={"front": ["HH", "HH"], "side": ["hhhhH", "ghhHH"],
                         "top": ["hh", "hh", "hh", "hH", "HH"]})

add("cow", "Cow Head", "Passive", size=COW,
    pal={".": "#4a3426", "d": "#36261c", "w": "#ece6dc", "W": "#cfc6b8", "k": "#101010",
         "m": "#c4b0a6", "M": "#9a8880", "n": "#4a3a34", "h": "#e2d8c4", "H": "#8a8070",
         "g": "#c0b49e", "f": "#ece6dc"},
    front=["d..ww..d",
           "...ww...",
           "w..www..",
           "wk.ww.k.",
           "...wW...",
           "d.....wd",
           "d......d",
           "dd....dd"],
    side=["d..ww.",
          "..www.",
          ".www..",
          "..ww..",
          "......",
          "d.....",
          "dd....",
          "ddd..d"],
    west=["dd....",
          "d.....",
          "......",
          "...ww.",
          "..www.",
          "d.ww..",
          "dd....",
          "ddd..d"],
    top=["dd....dd",
         "d.www..d",
         "..www...",
         "...ww...",
         "...ww...",
         "d..ww..d"],
    back=["dd....dd",
          "..www...",
          ".wwww...",
          "..ww....",
          "........",
          "........",
          "d......d",
          "dddddddd"],
    bottom_fill="d",
    extras=[COW_MUZZLE] + COW_HORNS,
    variants=[
        V("temperate", "Cow Head", {"minecraft:climate_variant": "temperate"}),
        V("warm", "Warm Cow Head", {"minecraft:climate_variant": "warm"},
          pal={".": "#a65e38", "d": "#844626", "w": "#ecd2aa", "W": "#d4b288",
               "m": "#dab49e", "M": "#b48c7a", "n": "#5a3a2c", "h": "#efe4cc", "H": "#4e4234",
               "g": "#cfc0a4"},
          extras=[COW_MUZZLE] + WARM_HORNS),
        V("cold", "Cold Cow Head", {"minecraft:climate_variant": "cold"},
          pal={".": "#94582e", "d": "#6a3c1e", "f": "#c47e46", "w": "#c47e46", "W": "#a8683a",
               "m": "#6e4c40", "M": "#4a3028", "n": "#24160f", "h": "#ece0c8", "H": "#9c8c74",
               "g": "#c8baa0"},
          front=["f.ff.ff.",
                 "f.f..f.f",
                 "fdf.ff.f",
                 "dk.ff.kd",
                 "..f..f..",
                 "f......f",
                 "d......d",
                 "fd....df"],
          side=["f.f.ff",
                "f.f.f.",
                "fdf.f.",
                "d.fdf.",
                "f.d.fd",
                "f.f.d.",
                "fdf.fd",
                "dfdfdf"],
          west=None,
          top=["f.ff.f.f",
               "f.f..f.f",
               "f.ff.f.f",
               "f.f..f.f",
               "f.ff.f.f",
               "f.ff.ff."],
          back=["f.ff.f.f",
                "f.f..f.f",
                "fdf.ff.f",
                "f.fd.f.d",
                "d.f..fdf",
                "f.ff.f.f",
                "fdf.dfdf",
                "dfdfdfdf"],
          extras=[COW_MUZZLE] + COLD_HORNS),
    ])

# --------------------------------------------------------------------------
# Horse and donkey share the vanilla horse head: 6x5x7 head, 4x5x5 muzzle,
# ears on top at the back, and the mane running over the top and down the
# back of the head.
# --------------------------------------------------------------------------
HORSE = (6, 5, 6)
HORSE_SIDE = ["d...d.",
              "....k.",
              "d.....",
              "dd....",
              "ddd.ll"]
HORSE_TOP = ["......",
             "d....d",
             "......",
             "......",
             "d....d",
             "......"]
HORSE_BACK = ["dd..dd",
              "d....d",
              "......",
              "d....d",
              "dd..dd"]
HORSE_MANE = [Cube((-1, 5, -1), (2, 1, 4), "m",
                   faces={"top": ["Mm", "mM", "Mm", "mm"], "front": ["mM"],
                          "side": ["MmMm"]}),
              Cube((-1, 0, 3), (2, 6, 1), "m",
                   faces={"back": ["mM", "Mm", "mM", "Mm", "mM", "Mm"],
                          "side": ["m", "M", "m", "M", "m", "M"], "top": ["mm"]})]


def horse_muzzle(letter=".", front=None, side=None, top=None):
    return snout(HORSE, (4, 5, 5), 0, letter,
                 faces={"front": front or ["....", "....", "n..n", ".ll.", "dddd"],
                        "side": side or [".....", ".....", "....n", "dddd.", "lllll"],
                        "top": top or ["....", "d..d", "....", "....", "...."],
                        "bottom": solid(4, 5, "d")})


add("donkey", "Donkey Head", "Passive", size=HORSE,
    pal={".": "#8a7a6a", "d": "#6a5c4e", "l": "#bcae9c", "L": "#d6cabb", "m": "#4a3e34",
         "M": "#5e5044", "n": "#3a3028", "k": "#101010", "e": "#a8988a", "i": "#c8b8aa"},
    front=["dd..dd", "d....d", "d....d", "d....d", "dd..dd"],
    side=HORSE_SIDE, top=HORSE_TOP, back=HORSE_BACK, bottom_fill="d",
    extras=[horse_muzzle("l", front=["....", "LllL", "nLLn", "llll", "dddd"],
                         side=[".....", "....L", "....n", "dddd.", "....."],
                         top=["....", "....", "....", "....", "L..L"])]
    + HORSE_MANE
    + pair(-3, 4, 2, (2, 7, 1), "e",
           faces={"front": ["dd", ".d", "id", "id", "i.", "..", ".."],
                  "back": ["dd", "d.", ".d", "..", "..", "..", ".."],
                  "side": ["d", "d", ".", ".", ".", ".", "."], "top": ["dd"]}))

# --------------------------------------------------------------------------
# Frog: flat 7x4x9 head (upper jaw plus a hint of the chin) with two
# bulging 3x2x3 eyes on top.
# --------------------------------------------------------------------------
FROG = (7, 4, 9)


def frog_pal(base, shade, spot, belly, mouth, light):
    return {".": base, "d": shade, "s": spot, "l": belly, "m": mouth, "L": light, "k": "#141414"}


add("frog", "Frog Head", "Passive", size=FROG,
    pal=frog_pal("#d0743e", "#a8562a", "#b45e2c", "#f0d0a0", "#5a2a14", "#e8a06a"),
    front=["...d...",
           "d.....d",
           "mmmmmmm",
           "lllllll"],
    side=["s..s..d..",
          "..s...s.d",
          "mmmmmmmmm",
          "lllllllll"],
    top=["..d.d..",
         "d..s..d",
         "..s.s..",
         "s.....s",
         ".s.d.s.",
         "d..s..d",
         "...s...",
         "...d...",
         "d.....d"],
    back=["..d.d..",
          "d.....d",
          "mmmmmmm",
          "lllllll"],
    bottom_fill="l",
    extras=pair(-3.5, 4, -3.5, (3, 2, 3), ".",
                faces={"front": ["L..", "kk."], "side": ["..L", ".kk"],
                       "back": ["...", "..."], "top": ["...", ".L.", "L.."]}),
    variants=[
        V("temperate", "Temperate Frog Head", {"variant": 0}),
        V("cold", "Cold Frog Head", {"variant": 1},
          pal=frog_pal("#6e9a44", "#4e7430", "#557d34", "#dcd8a4", "#2a3a18", "#96be68")),
        V("warm", "Warm Frog Head", {"variant": 2},
          pal=frog_pal("#e8dcc2", "#c8b896", "#b8a07a", "#f8f2e4", "#6a5440", "#fbf6ea")),
    ])

# --------------------------------------------------------------------------
# Glow squid: the whole body is the head, scaled down to 8x8x8. Tentacles
# hang below the block, so they are only hinted at along the bottom.
# --------------------------------------------------------------------------
add("glow_squid", "Glow Squid Head", "Passive",
    pal={".": "#155a63", "d": "#0e4048", "D": "#0a2e34", "c": "#6ff2d8", "C": "#c8fff4",
         "g": "#2f9a96", "k": "#0a1a1e"},
    front=["d......d",
           "..c..g..",
           "g......c",
           "........",
           ".CC..CC.",
           ".Ck..kC.",
           "..g..g..",
           "DgDgDgDg"],
    side=["d......d",
          "..g...c.",
          "........",
          ".c...g..",
          "........",
          "...g...c",
          "g.....g.",
          "DgDgDgDg"],
    top=["dddddddd",
         "d..g...d",
         ".c....g.",
         "...cc...",
         "...cc...",
         ".g....c.",
         "d...g..d",
         "d......d"],
    back=["d......d",
          ".g...c..",
          "......g.",
          "..c.....",
          ".....c..",
          "g.......",
          "..g..g..",
          "DgDgDgDg"],
    bottom=["DgDgDgDg",
            "g......D",
            "D.dddd.g",
            "g.dkkd.D",
            "D.dkkd.g",
            "g.dddd.D",
            "D......g",
            "gDgDgDgD"])

# --------------------------------------------------------------------------
# Happy ghast: a 16x16x16 body in vanilla, drawn here at 10x10x10. Its
# tentacles are hinted at along the bottom edge and on the underside.
# --------------------------------------------------------------------------
add("happy_ghast", "Happy Ghast Head", "Passive", size=(10, 10, 10),
    pal={".": "#f3f1ee", "s": "#e0dcd8", "S": "#c6c0ba", "k": "#1c1c24", "w": "#ffffff",
         "p": "#f4a6b8", "m": "#5a4048"},
    front=["s........s",
           "..........",
           "..........",
           "..wk..wk..",
           "..kk..kk..",
           "..kk..kk..",
           ".pp....pp.",
           "....mm....",
           "s........s",
           "sSsSsSsSsS"],
    side=["ss.......s",
          "s.........",
          "......s...",
          "..........",
          "...s......",
          ".........s",
          "s.....s...",
          "..........",
          "ss.......s",
          "SsSsSsSsSs"],
    top=["ss....s.ss",
         "s........s",
         "....s.....",
         "..........",
         ".s.....s..",
         "..........",
         "...s......",
         "........s.",
         "s.........",
         "s........s"],
    back=["ss......ss",
          "s........s",
          "...s......",
          "..........",
          ".......s..",
          "..s.......",
          "..........",
          ".....s....",
          "s........s",
          "sSsSsSsSsS"],
    bottom=["ssssssssss",
            "sSS.SS.SSs",
            "sSS.SS.SSs",
            "s........s",
            "sSS.SS.SSs",
            "sSS.SS.SSs",
            "s........s",
            "sSS.SS.SSs",
            "sSS.SS.SSs",
            "ssssssssss"])

# --------------------------------------------------------------------------
# Horse: same head as the donkey with short ears; the coat colour changes
# per variant and the mane follows it.
# --------------------------------------------------------------------------


def horse_pal(base, shade, light, mane, mane_shade, nose, eye="#101010"):
    return {".": base, "d": shade, "l": light, "m": mane, "M": mane_shade, "n": nose,
            "k": eye}


add("horse", "Horse Head", "Passive", size=HORSE,
    pal=horse_pal("#7a4a26", "#5e3618", "#9a6438", "#2a1a10", "#3e2818", "#2a1810"),
    front=["dd..dd", "d....d", "d....d", "d....d", "dd..dd"],
    side=HORSE_SIDE, top=HORSE_TOP, back=HORSE_BACK, bottom_fill="d",
    extras=[horse_muzzle()] + HORSE_MANE
    + pair(-3, 5, 2, (2, 3, 1), ".",
           faces={"front": ["d.", "dl", ".."], "back": [".d", "..", ".."],
                  "side": ["d", ".", "."], "top": ["dd"]}),
    variants=[
        V("brown", "Brown Horse Head", {"variant": 3}),
        V("white", "White Horse Head", {"variant": 0},
          pal=horse_pal("#e4e0d6", "#c4beb2", "#f6f4ee", "#cfcac2", "#aea9a0", "#6a6460")),
        V("creamy", "Creamy Horse Head", {"variant": 1},
          pal=horse_pal("#d4b47e", "#b8965e", "#e8cc9c", "#ece0c4", "#c8b896", "#5a4632")),
        V("chestnut", "Chestnut Horse Head", {"variant": 2},
          pal=horse_pal("#a65e2e", "#84461e", "#c27a44", "#7a3c18", "#5e2c10", "#3a2010")),
        V("black", "Black Horse Head", {"variant": 4},
          pal=horse_pal("#2e2a28", "#1e1a18", "#48423e", "#121010", "#24201e", "#0e0c0c",
                        eye="#000000")),
        V("gray", "Gray Horse Head", {"variant": 5},
          pal=horse_pal("#8a8a88", "#6e6e6c", "#a8a8a6", "#3a3a3a", "#505050", "#2e2e2e")),
        V("dark_brown", "Dark Brown Horse Head", {"variant": 6},
          pal=horse_pal("#4a3020", "#382214", "#604232", "#1e130b", "#2e1e14", "#1a100a")),
    ])
