"""Head art: Hostile mobs, part 1 (blaze to husk).

See tools/mobs.py for the coordinate system and the art conventions.
"""

from mobs import K, W, Cube, V, add, pair, snout  # noqa: F401


def tile(pattern, w, h, dx=0, dy=0):
    """Crop a w x h window out of a repeating pattern (for big scaly faces)."""
    ph, pw = len(pattern), len(pattern[0])
    return ["".join(pattern[(y + dy) % ph][(x + dx) % pw] for x in range(w))
            for y in range(h)]


def frame(art, ch):
    """Paint a one pixel border of `ch` around a face."""
    h = len(art)
    return [ch * len(row) if y in (0, h - 1) else ch + row[1:-1] + ch
            for y, row in enumerate(art)]


# --------------------------------------------------------------------------
# Blaze: 8x8x8 golden head, dark eyes with a glowing core, smoky mottling
# that darkens towards the bottom.
# --------------------------------------------------------------------------
add("blaze", "Blaze Head", "Hostile",
    pal={".": "#f0b22a", "y": "#ffd95a", "Y": "#fff3a8", "o": "#d97c1b",
         "O": "#a44f10", "k": "#2a1006", "e": "#fff7c8"},
    front=["yyYyyYyy",
           "Y......Y",
           ".o....o.",
           ".kk..kk.",
           ".ke..ek.",
           "o......o",
           ".oOOOOo.",
           "o.o..o.o"],
    side=["y.yy.Yy.",
          ".o..y..o",
          "o.Oo..o.",
          ".o..o.O.",
          "y..O..o.",
          ".oO.o..o",
          "O..oO.O.",
          ".O.O..oO"],
    top=["yY.yy.Yy",
         ".y.Yy.y.",
         "yo.y..oy",
         ".yy.oy..",
         "y.oy.yy.",
         ".yY..oy.",
         "y.y.Yy.y",
         "yy.yy.yy"],
    back=["yy.y.Yyy",
          ".o.yo..o",
          "o.O.o.O.",
          ".o..O.o.",
          "O.oo..oO",
          ".O..oO.o",
          "oO.O..Oo",
          "O.oO.OO."],
    bottom_fill="O")

# --------------------------------------------------------------------------
# Bogged: sage green skeleton skull, moss over the top running down the
# back, a red and a brown mushroom growing out of the crown.
# --------------------------------------------------------------------------
add("bogged", "Bogged Skull", "Hostile",
    pal={".": "#a6b18c", "s": "#88946e", "S": "#6b7756", "k": "#1c2317",
         "g": "#4d7b2d", "G": "#78a547", "v": "#33561f",
         "r": "#c42e26", "R": "#8c1d18", "w": "#f2ead8",
         "m": "#9a6f4e", "M": "#6c4d35", "n": "#b98e66", "t": "#ddd2b6"},
    front=["gGggGgGg",
           "vg.s.gvg",
           "g......v",
           ".kk..kk.",
           ".kk..kk.",
           "v..kk...",
           ".kSkkSk.",
           "v.s..s.g"],
    side=["GgGgggGg",
          "vgv.g.gv",
          "v.g...s.",
          "g..s....",
          "v.....S.",
          ".v..s...",
          "v.....s.",
          "..s.s..."],
    top=["gGgGGgGg",
         "GgggGgGg",
         "g.gGg.gG",
         "Gg..gGg.",
         "g.G...gg",
         ".g.s..g.",
         "gGg..gGg",
         "gGggGgGg"],
    back=["gGgGgGgG",
          "gvgGvggv",
          "v.vg.gv.",
          "v..v..v.",
          "..sv..v.",
          "v...s...",
          "....v..s",
          ".s...s.."],
    bottom_fill="s",
    extras=[
        # Red mushroom, front left of the crown.
        Cube((-2.5, 8, -2.5), (1, 1, 1), "t"),
        Cube((-3.5, 9, -3.5), (3, 2, 3), "r",
             faces={"front": ["rwr", "RRR"], "side": ["wrr", "RRR"],
                    "back": ["rrw", "RRR"], "top": ["rwr", "wrr", "rrw"],
                    "bottom": ["RtR", "ttt", "RtR"]}),
        # Brown mushroom, back right: thin stem and a flat wide cap.
        Cube((2, 8, 1.5), (1, 2, 1), "t"),
        Cube((0.5, 10, 0), (4, 1, 4), "m",
             faces={"front": ["MmmM"], "side": ["MmmM"], "back": ["MmmM"],
                    "top": ["mnmm", "nmmn", "mmnm", "mnmm"],
                    "bottom": ["MMMM", "MttM", "MttM", "MMMM"]}),
    ])

# --------------------------------------------------------------------------
# Breeze: pale periwinkle head with wind swirls, wrapped by the wide dark
# eye band (10x3x4 in vanilla) holding two glowing eyes.
# --------------------------------------------------------------------------
add("breeze", "Breeze Head", "Hostile",
    pal={".": "#aab5ea", "l": "#d6dcfa", "L": "#f2f5ff", "d": "#7c82cc",
         "D": "#5a5aa8", "p": "#3a3070", "P": "#54469c", "e": "#effcff",
         "c": "#8fe0ff"},
    front=["lLl.ldl.",
           ".l.dl..d",
           "d.l..l..",
           "dddddddd",
           "dddddddd",
           "dddddddd",
           ".d..ld.l",
           "l.dl..d."],
    side=["l..lL..l",
          ".ll..ll.",
          "........",
          "d..dd..d",
          ".dd..dd.",
          "........",
          "l..ll..l",
          ".ll..ll."],
    top=["ddddddl.",
         "d....dl.",
         "d.dd.dl.",
         "d.dL.dl.",
         "d.dddd.l",
         "d......l",
         "dddddddl",
         "lllllll."],
    back=["l.lLl.ll",
          ".l..l..d",
          "dd....dd",
          "..dddd..",
          "l......l",
          ".ll..ll.",
          "d..dd..d",
          ".dd..dd."],
    bottom_fill="d",
    extras=[Cube((-5, 2, -4.5), (10, 3, 4), "p",
                 faces={"front": ["pPeePPeePp",
                                  "pPccPPccPp",
                                  "pppPPPPppp"],
                        "side": ["PPpp", "pPpP", "pppp"],
                        "top": ["DDDDDDDDDD", "pppppppppp", "PpPpPpPpPp", "pPPPPPPPPp"]})])

# --------------------------------------------------------------------------
# Camel husk: the camel head (tall 7 wide head with a long 5x5 muzzle on
# top and sideways ears) in dry, cracked husk colours with sunken eyes.
# --------------------------------------------------------------------------
CAMEL_HUSK = (7, 10, 6)
add("camel_husk", "Camel Husk Head", "Hostile", size=CAMEL_HUSK,
    pal={".": "#b39c71", "s": "#94805a", "S": "#6f5f40", "l": "#cdb98c",
         "g": "#8d8c62", "k": "#1c160e", "e": "#7a6236", "n": "#3a2e1e",
         "m": "#4b3c27"},
    front=["l.....l",
           "s.....s",
           ".......",
           "s.....s",
           ".......",
           "ss.s.ss",
           "..s.s..",
           ".s...s.",
           "s..g..s",
           "Ss.s.sS"],
    side=["l.l.l.",
          ".s..S.",
          "s..kk.",
          ".s.ke.",
          "g..SS.",
          "s.s...",
          ".s.g.s",
          "s.s...",
          ".S.s.s",
          "SsS.sS"],
    top=["ll.l.ll",
         ".s..g.s",
         "l..s...",
         ".g...s.",
         "s..l..g",
         ".s.g.s."],
    back=["l.lSl.l",
          ".s.S.s.",
          "s..S..s",
          "..sS.g.",
          ".g.S...",
          "s..S.s.",
          "..sS..s",
          ".s.S.g.",
          "s..S..s",
          "SsSSSsS"],
    bottom_fill="s",
    extras=[snout(CAMEL_HUSK, (5, 5, 5), 5, ".",
                  faces={"front": ["l.l.l", "nl.ln", "..s..", "mmSmm", "s.s.s"],
                         "side": ["l.l.l", "..s.n", "s..s.", "Smmmm", ".s.s."],
                         "top": ["s.l.s", "..s..", "l...l", ".s.s.", "sl.ls"],
                         "bottom": ["sSsSs", "SsSsS", "sSsSs", "SsSsS", "sSsSs"]})]
    + pair(-6.5, 8.5, 0.5, (3, 1, 2), "s",
           faces={"top": ["sSs", "lsS"], "front": ["sSs"], "side": ["Ss"]}))

# --------------------------------------------------------------------------
# Cave spider: the 8x8x8 spider head in dark teal with eight red eyes (two
# big ones, six small) and a pair of fangs under the face.
# --------------------------------------------------------------------------
add("cave_spider", "Cave Spider Head", "Hostile",
    pal={".": "#163f47", "d": "#0c2a30", "l": "#2a6a6e", "L": "#3f8a86",
         "r": "#a8141a", "R": "#e02b2b", "h": "#ff9a9a", "f": "#7d8a7c", "F": "#2e3a33"},
    front=[".d.dd.d.",
           "d......d",
           "..r..r..",
           "rhR..Rhr",
           ".RR..RR.",
           "...rr...",
           ".d....d.",
           "d.dFFd.d"],
    side=["l.L..l.l",
          ".d..d...",
          "l..l....",
          ".d...d..",
          "...l..l.",
          "d.d.....",
          ".d..dd.d",
          "dd.d.dd."],
    top=["d.l..l.d",
         ".d.ll.d.",
         "l..dd..l",
         ".l.dd.l.",
         "d..LL..d",
         ".d....d.",
         "l.l..l.l",
         ".d.dd.d."],
    back=["dl.dd.ld",
          ".d.ll.d.",
          "l.d..d.l",
          ".dddddd.",
          ".dddddd.",
          "l.dddd.l",
          ".d....d.",
          "dd.l.ldd"],
    bottom_fill="d",
    extras=pair(-2, 0, -5, (1, 2, 1), "F", faces={"front": ["F", "f"], "side": ["F", "f"]}))

# --------------------------------------------------------------------------
# Creaking: tall 6x13x6 bark head with deep sockets and glowing orange
# eyes; crooked twigs branch off both sides and the crown.
# --------------------------------------------------------------------------
add("creaking", "Creaking Head", "Hostile", size=(6, 13, 6),
    pal={".": "#4a3f36", "d": "#2e2620", "D": "#1b1511", "l": "#6b5e52",
         "L": "#8c7f70", "o": "#ff8a1a", "y": "#ffd65a", "b": "#3b3028",
         "B": "#5e4f41", "g": "#9a9e8c"},
    front=["lL.dLl",
           ".l.d.l",
           "l..d..",
           ".l.dl.",
           "DDldDD",
           "Dy.dyD",
           "Do.doD",
           "DD.dDD",
           ".l.d.l",
           "l.Dd..",
           ".DDDD.",
           "l.d..l",
           ".ld.L."],
    side=["l.dl.d",
          ".Dl.dD",
          "d.l.D.",
          ".D.ld.",
          "l.d.Dg",
          ".D.l.d",
          "d.lD.L",
          ".D.d.l",
          "l.d.D.",
          ".D.ld.",
          "d.l.D.",
          "lD.d.l",
          "dDdDdD"],
    top=["lldll.",
         "l.dd.l",
         "d.LL.d",
         "d.LL.d",
         "l.dd.l",
         ".llld."],
    back=["d.lDl.",
          ".dL.dl",
          "lD.d.D",
          ".d.lD.",
          "D.dl.d",
          "l.D.dl",
          ".dlD.d",
          "dl.d.D",
          ".D.ld.",
          "l.d.Dl",
          "dD.l.d",
          ".l.dD.",
          "DdDdDd"],
    bottom_fill="d",
    extras=[
        # Right side: a long branch that kinks up, plus a short low twig.
        Cube((3, 9, -0.5), (2, 1, 1), "b"),
        Cube((5, 9, -0.5), (1, 3, 1), "b"),
        Cube((6, 11, -0.5), (2, 1, 1), "B"),
        Cube((3, 4, 0), (2, 1, 1), "b"),
        Cube((5, 4, 0), (1, 2, 1), "B"),
        # Left side.
        Cube((-5, 7, -0.5), (2, 1, 1), "b"),
        Cube((-6, 7, -0.5), (1, 4, 1), "b"),
        Cube((-8, 10, -0.5), (2, 1, 1), "B"),
        Cube((-5, 2, 0), (2, 1, 1), "b"),
        # Crown twigs.
        Cube((1, 13, -0.5), (1, 2, 1), "b"),
        Cube((2, 14, -0.5), (1, 1, 1), "B"),
        Cube((-2, 13, 0.5), (1, 1, 1), "B"),
    ])

# --------------------------------------------------------------------------
# Drowned: teal zombie head with glowing cyan eyes and seaweed hair
# draped over the top, the sides and down the back.
# --------------------------------------------------------------------------
add("drowned", "Drowned Head", "Hostile",
    pal={".": "#5aa39a", "d": "#3e8079", "D": "#2b5e59", "c": "#6fe8e2",
         "C": "#e2fffd", "k": "#14302d", "g": "#3d7a2b", "G": "#62a03c",
         "n": "#2f6a64"},
    front=["gGgDgGgg",
           "g.gd.gDg",
           "D.d...g.",
           ".Cc..cC.",
           "...d....",
           "d..nn..d",
           ".dkkkkd.",
           "..d..g.."],
    side=["gGgGggGg",
          "gg.gGg.g",
          "g.Gg.g..",
          "Gg..d...",
          "g.g.....",
          ".g..d..d",
          "g.d.....",
          ".d..d.d."],
    top=["gGgGgGgg",
         "GggGgggG",
         "gGgggGgg",
         "gg.GgggG",
         "Ggg.gGgg",
         "gGgggg.g",
         "ggGg.Ggg",
         "gGggGgGg"],
    back=["gGgGggGg",
          "gggGgGgg",
          "Gg.gGg.g",
          "g.gg.gg.",
          ".g.g..g.",
          "g..g...g",
          ".d.g..d.",
          "d..d.d.."],
    bottom_fill="d",
    extras=[Cube((1, 8, -1), (1, 2, 1), "G"), Cube((-3, 8, 1), (1, 1, 1), "g")])

# --------------------------------------------------------------------------
# Guardian family: a scaled down guardian body with the side and top fin
# plates, spikes sticking out of every plate, the big single eye with a
# protruding pupil, and a tail stub. Elder guardians are bigger.
# --------------------------------------------------------------------------
GUARDIAN_SCALES = ["..o.d..l..d.",
                   ".oOo...l...d",
                   "..o..d...o..",
                   "d...ll..oOo.",
                   "..d....d.o..",
                   ".l..o.....d.",
                   ".l.oOo.d..l.",
                   "....o...d.l.",
                   "d.d....o....",
                   "...l..oOo.d.",
                   ".o.l...o....",
                   "oOo..d...l.."]


def guardian(key, name, pal, size, front):
    w, h, d = size
    pd = d - 2                      # fin plates are shorter than the body
    spike = []

    def spike_at(base, tip):
        spike.append(Cube(base, (1, 1, 1), "s"))
        spike.append(Cube(tip, (1, 1, 1), "S"))

    # Four spikes on the top plate, at its edges.
    for x, z in ((-0.5, -pd / 2), (-0.5, pd / 2 - 1), (-(w - 2) / 2, -0.5), ((w - 2) / 2 - 1, -0.5)):
        spike_at((x, h + 1, z), (x, h + 2, z))
    # Two spikes out of each side plate, near the front and the back.
    y = h / 2 - 0.5
    for z in (-pd / 2, pd / 2 - 1):
        spike_at((w / 2 + 1, y, z), (w / 2 + 2, y, z))
        spike_at((-w / 2 - 2, y, z), (-w / 2 - 3, y, z))

    plate_side = frame(tile(GUARDIAN_SCALES, pd, h - 2, 3, 1), "d")
    plate_top = frame(tile(GUARDIAN_SCALES, w - 2, pd, 5, 2), "d")
    tw = w // 2
    tl = 7 - d // 2                 # tail length that still fits the block
    extras = [
        Cube((w / 2, 1, -pd / 2), (1, h - 2, pd), ".",
             faces={"side": plate_side, "top": ["d" * 1] * pd}),
        Cube((-w / 2 - 1, 1, -pd / 2), (1, h - 2, pd), ".",
             faces={"side": plate_side, "top": ["d" * 1] * pd}),
        Cube((-(w - 2) / 2, h, -pd / 2), (w - 2, 1, pd), ".",
             faces={"top": plate_top, "front": ["d" * (w - 2)], "back": ["d" * (w - 2)]}),
        # The pupil sits proud of the eye.
        Cube((-1, h / 2 - 1, -d / 2 - 1), (2, 2, 1), "p", faces={"front": ["Wp", "pp"]}),
        # Tail stub with an orange fin tip.
        Cube((-tw / 2, h / 4, d / 2), (tw, tw, tl), ".",
             faces={"back": frame(tile(GUARDIAN_SCALES, tw, tw, 1, 4), "d"),
                    "side": tile(GUARDIAN_SCALES, tl, tw, 7, 0),
                    "top": tile(GUARDIAN_SCALES, tw, tl, 2, 6)}),
        Cube((-1, h / 4 + tw / 2 - 1, d / 2 + tl), (2, 2, 1), "o",
             faces={"back": ["Oo", "oO"]}),
    ] + spike
    add(key, name, "Hostile", size=size, pal=pal, front=front,
        side=frame(tile(GUARDIAN_SCALES, d, h, 0, 3), "d"),
        top=frame(tile(GUARDIAN_SCALES, w, d, 4, 0), "d"),
        back=frame(tile(GUARDIAN_SCALES, w, h, 6, 5), "d"),
        bottom=frame(tile(GUARDIAN_SCALES, w, d, 2, 7), "d"),
        extras=extras)


guardian("elder_guardian", "Elder Guardian Head",
         {".": "#cfc8b2", "d": "#a29a83", "l": "#e8e3d2", "o": "#8f7f9c",
          "O": "#ab9bb6", "w": "#f1ecf3", "k": "#6e6758", "p": "#4a2e5c",
          "W": "#ffffff", "s": "#e6dfd2", "S": "#fbf8f2"},
         (10, 10, 12),
         ["d.o.ll.o.d",
          ".o..dd..o.",
          "..kkkkkk..",
          ".lkwwwwkl.",
          ".lkwwwwkl.",
          ".lkwwwwkl.",
          ".lkwwwwkl.",
          "..kkkkkk..",
          ".o..dd..o.",
          "d.o....o.d"])

# --------------------------------------------------------------------------
# Endermite: its head segment scaled up, dark violet shell with lilac
# speckles, tiny magenta eyes and two little mandibles.
# --------------------------------------------------------------------------
add("endermite", "Endermite Head", "Hostile", size=(6, 4, 5),
    pal={".": "#2e2238", "d": "#1a1222", "p": "#6b4a8a", "P": "#a77ad0",
         "e": "#d04cff"},
    front=["P.pp.P",
           ".e..e.",
           "d.dd.d",
           ".d..d."],
    side=["P.p.p",
          "..d..",
          "d.p.d",
          ".dd.d"],
    top=["p.P.p.",
         ".d..dP",
         "P..p..",
         ".p.d.p",
         "p.P..P"],
    back=["pP..Pp",
          ".d.p.d",
          "d.dd.d",
          "dd..dd"],
    bottom_fill="d",
    extras=pair(-2, 0, -3.5, (1, 1, 1), "d", faces={"front": ["p"]}))

# --------------------------------------------------------------------------
# Evoker: tall 8x10x8 illager head with the long 2x4x2 nose, dark hair
# hooding the top, sides and back, a heavy unibrow over green eyes and the
# black and gold robe collar at the bottom.
# --------------------------------------------------------------------------
EVOKER = (8, 10, 8)
add("evoker", "Evoker Head", "Hostile", ["minecraft:evocation_illager"], size=EVOKER,
    pal={".": "#a3a8a3", "s": "#868b87", "l": "#bec3be", "h": "#26262a",
         "H": "#3e3e44", "b": "#2e2e30", "w": "#ececec", "g": "#2f8a3c",
         "n": "#949994", "N": "#6f7470", "y": "#d8ab35", "k": "#18181c"},
    front=["hhHhhHhh",
           "hH.hh.Hh",
           "h..l...h",
           ".bbbbbb.",
           ".wg..gw.",
           "s......s",
           "s..nn..s",
           ".s....s.",
           "s.N..N.s",
           "kys..syk"],
    side=["hhhhhhhh",
          "hhHhhhHh",
          "hHhhhH.h",
          "hhhHh...",
          "hHhh....",
          "hhH..s..",
          "hh.....s",
          "hH..s...",
          "hh.s...s",
          "kykkykky"],
    top=["hHhhHhhh",
         "hhhHhhHh",
         "HhhhhhhH",
         "hhHhhHhh",
         "hHhhhhhh",
         "hhhHhHhh",
         "Hhhhhhhh",
         "hhHhhhHh"],
    back=["hhHhhhHh",
          "hHhhHhhh",
          "hhhHhhHh",
          "HhhhhHhh",
          "hhHhhhhH",
          "hHhHhhHh",
          "s.hhhh.s",
          ".s....s.",
          "kkykkykk",
          "ykkyykky"],
    bottom_fill="k",
    extras=[snout(EVOKER, (2, 4, 2), 0, "n",
                  faces={"front": ["nn", "nn", "nn", "NN"],
                         "side": ["nn", "nn", "nN", "NN"],
                         "top": ["nn", "nn"]})])

# --------------------------------------------------------------------------
# Ghast: the 16 pixel cube scaled to 10, pale with grey wisps, closed eyes
# with tear tracks and a small sad mouth; tentacle roots underneath.
# --------------------------------------------------------------------------
add("ghast", "Ghast Head", "Hostile", size=(10, 10, 10),
    pal={".": "#f1f0f0", "s": "#dcdbdb", "S": "#bdbcbc", "k": "#6a6a6a",
         "K": "#3e3e3e", "t": "#a7aab4"},
    front=["..........",
           "..s....s..",
           "..........",
           ".KKK..KKK.",
           "..t....t..",
           "..t....t..",
           ".........s",
           "...kkkk...",
           "...kKKk...",
           ".s......s."],
    side=["..s.......",
          ".....s....",
          ".s......s.",
          "....s.....",
          "s......s..",
          "...s......",
          "......s..s",
          ".s..S.....",
          "....s..s..",
          "s.S..S..S."],
    top=["...s......",
         ".s....s...",
         ".........s",
         "..s.......",
         ".....s..s.",
         "s.........",
         "...s...s..",
         "..........",
         ".s..s.....",
         "......s..s"],
    back=["......s...",
          ".s.......s",
          "....s.....",
          "..s....s..",
          "s.........",
          ".....s..s.",
          "..s.......",
          "......S...",
          ".S..s...s.",
          "s..S..S..S"],
    bottom=["..........",
            ".SS.SS.SS.",
            ".SS.SS.SS.",
            "..........",
            ".SS.SS.SS.",
            ".SS.SS.SS.",
            "..........",
            ".SS.SS.SS.",
            ".SS.SS.SS.",
            ".........."])

guardian("guardian", "Guardian Head",
         {".": "#5d9f8c", "d": "#3f7465", "l": "#86c6b0", "o": "#c46a2e",
          "O": "#e1914a", "w": "#f2e6dc", "k": "#2c4f46", "p": "#3b1f14",
          "W": "#ffffff", "s": "#e8dcc0", "S": "#fff6e2"},
         (8, 8, 10),
         ["d.o..o.d",
          ".kkkkkk.",
          "lkwwwwkl",
          "lkwwwwkl",
          "lkwwwwkl",
          "lkwwwwkl",
          ".kkkkkk.",
          "d.o..o.d"])

# --------------------------------------------------------------------------
# Hoglin: wide 10x8x8 skull with a broad pink snout, tall tusks either side
# of it, drooping ears and a blond bristly mane along the top.
# --------------------------------------------------------------------------
HOGLIN = (10, 8, 8)
add("hoglin", "Hoglin Head", "Hostile", size=HOGLIN,
    pal={".": "#c4876a", "s": "#a56a50", "S": "#7d4c37", "l": "#dca186",
         "k": "#1f1410", "e": "#a86c52", "E": "#e0a18f", "n": "#e0a594",
         "N": "#5a2e26", "t": "#efe5cc", "T": "#c9b994", "m": "#d9b26c",
         "M": "#b08646"},
    front=["l.s.mm.s.l",
           ".s..ss..s.",
           ".kS....Sk.",
           "s........s",
           "s........s",
           "S........S",
           "s........s",
           "SS......SS"],
    side=["l.ll.l.l",
          ".s..s..s",
          "s..s.sSk",
          ".s..s.s.",
          "s.s..s.s",
          ".S.s..S.",
          "S..S.S.S",
          "SS.SS.SS"],
    top=["s.ls..sl.s",
         ".l.s..s.l.",
         "l.s....s.l",
         ".s.l..l.s.",
         "s..s..s..s",
         ".l.s..s.l.",
         "l.s....s.l",
         "l.s.ll.s.l"],
    back=["s.l.mm.l.s",
          ".s..mM..s.",
          "s.s.Mm.s.s",
          ".s..mm..s.",
          "s..s..s..s",
          ".S.s..s.S.",
          "S.S.SS.S.S",
          "SS.SSSS.SS"],
    bottom_fill="S",
    extras=[snout(HOGLIN, (8, 5, 4), 0, "n",
                  faces={"front": ["l.l..l.l",
                                   ".NN..NN.",
                                   ".NN..NN.",
                                   "........",
                                   "s.SSSS.s"],
                         "side": ["..l.", ".l..", "....", "SSSS", "..s."],
                         "top": ["s.s..s.s", "..l..l..", "l..ll..l", ".l....l."]})]
    + pair(-5, 1, -8, (1, 5, 1), "t",
           faces={"front": ["t", "t", "t", "T", "T"], "side": ["t", "t", "T", "T", "T"]})
    # Ears: a flap out to the side with a drooping tip.
    + pair(-7, 6, -2, (2, 1, 3), "e",
           faces={"top": ["ee", "eE", "ee"], "bottom": ["EE", "EE", "EE"]})
    + pair(-8, 5, -1.5, (1, 2, 2), "e", faces={"side": ["ee", "EE"]})
    # Mane: low at the brow, taller towards the back.
    + [Cube((-1, 8, -2.5), (2, 1, 3), "m",
            faces={"top": ["mM", "Mm", "mM"], "side": ["MmM"], "front": ["mM"]}),
       Cube((-1, 8, 0.5), (2, 2, 3), "m",
            faces={"top": ["Mm", "mM", "Mm"], "side": ["mMm", "MmM"],
                   "front": ["Mm", "mM"], "back": ["mM", "MM"]})])

# --------------------------------------------------------------------------
# Husk: sandy zombie head with dark wrapped hair, sunken black eyes and a
# shrivelled mouth.
# --------------------------------------------------------------------------
add("husk", "Husk Head", "Hostile",
    pal={".": "#b29f73", "s": "#988659", "S": "#776844", "l": "#c9b88c",
         "h": "#6d5a3a", "H": "#544428", "k": "#1d1a12", "K": "#3d3524",
         "n": "#5c4d33", "m": "#463a26"},
    front=["hHhhhHhh",
           "h.hHh.hH",
           "s.l..l.s",
           ".kK..Kk.",
           "s......s",
           "...nn...",
           ".smmmms.",
           "s.s..s.s"],
    side=["hhHhhHhh",
          "hHh.hhHh",
          "h.h.H..s",
          ".h...s..",
          "s..s...s",
          ".s...s..",
          "s..s..s.",
          ".S.s.S.s"],
    top=["hhHhhhHh",
         "HhhhHhhh",
         "hhHhhhHh",
         "hHhhHhhH",
         "hhhHhhhh",
         "HhhhhHhh",
         "hhHhhhhH",
         "hHhhHhhh"],
    back=["hHhhhHhh",
          "hhHhhhHh",
          "HhhhHhhH",
          "h.hHh.hh",
          ".h.h..h.",
          "s..s...s",
          ".s...s..",
          "S.sS.s.S"],
    bottom_fill="s")
