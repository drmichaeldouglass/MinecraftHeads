# Mob Trophies (Minecraft Bedrock add-on)

Every mob drops its head when a player kills it. Heads can be placed on top of a
block, mounted on a wall, hung from a ceiling like a trophy, or worn as a hat.
Collect one head from every mob in the game to become a **Trophy Master**, then
hunt down every variant.

![All the custom heads](docs/heads_preview.png)

![Heads worn by a player](docs/worn_preview.png)

## Features

- **205 heads**: 199 custom heads for 82 mobs plus the 6 vanilla heads
  (creeper, zombie, skeleton, wither skeleton, piglin, ender dragon), which drop
  as the real vanilla items.
- **One head per mob variant**: every cat breed, wolf coat, sheep colour, horse
  colour, llama, parrot, rabbit, axolotl, frog, fox, mooshroom and panda
  personality, the warm and cold cows, pigs and chickens, copper golem
  oxidation stages, villager and zombie villager biomes, shulker colours,
  tropical fish patterns and the coral zombie nautilus. The head that drops
  matches the mob you killed.
- **Detailed heads**: each head follows the shape of the mob's in-game head
  (snouts, beaks, ears, horns, tusks, fins, hats) with pixel art on every side.
- **Placement like vanilla skulls**: stand a head on a block (it turns to face
  you), mount it on the side of a block, or hang it underneath one.
- **Wear them**: put a head in your helmet slot to wear it. It is drawn scaled
  up over your own head.
- **Mob abilities**: every head grants powers while worn. All variants of a
  mob share its powers, including the six vanilla heads. Fly with a Bat head,
  climb walls with a Spider head, teleport with an Enderman head, breathe
  underwater with aquatic heads, or use a Creeper blast.
- **Collection tracking**: a head counts as collected the first time it lands in
  your inventory or helmet slot. A mob counts towards the collection once you
  have any of its variants; every variant is tracked too. Progress is saved per
  player in the world.
- **Trophy Ledger**: new players get a Trophy Ledger book. Use it to see your
  progress, split into Passive, Neutral, Hostile and Boss mobs, with a page per
  mob listing its variants. Lost it? Craft a new one from a **book + bone**.
- **Completion reward**: collecting all 87 required heads shows a title and
  announces it to everyone in the world.

### Special cases

| Mob | How to get the head |
| --- | --- |
| Creaking | Break its active Creaking Heart while the creaking is nearby. |
| Ender Dragon, Wither | Drops if a player is nearby when it dies, even if the final blow was an explosion. |
| Villager, Zombie Villager | Both the old and new villager entity types count. |
| Sulfur Cube | Bonus head. It is still experimental, so it does not count towards the 87. |

All other mobs must be killed by a player (melee, arrows, tridents and other
projectiles all count). Baby mobs drop heads too.

## Installing

**iPhone / iPad / Windows / Android:** download
[`dist/MobTrophies.mcaddon`](dist/MobTrophies.mcaddon) and open it. Minecraft
imports both packs. Then, when creating or editing a world, activate
**Mob Trophies** under *Behavior Packs* (the resource pack is added for you).

Requires Minecraft Bedrock **1.21.90 or newer**. No experimental toggles are
needed.

### Using head powers (version 1.2.0)

Equip the head in the **helmet slot**. Carrying it or placing it as a trophy
does not grant powers. A message tells you the ability when you equip it;
the Trophy Ledger category pages also explain every mob's powers.

- **Passive traits** activate automatically, such as strength, jumping,
  fire resistance and underwater breathing.
- **Crouch once** to activate a special attack or teleport. Release crouch
  before using it again. Each mob has a cooldown, shared by all its variants.
- **Flying heads**: hold Jump to rise, use movement controls to steer, release
  Jump to glide down, and crouch to descend. This works in Survival without
  changing game mode.
- **Spider / Cave Spider**: face a wall and hold Jump to climb.
- **Aquatic heads**: use the normal swimming controls for a swimming boost.
- **Melee traits**, such as Cave Spider poison or Wither Skeleton Wither,
  apply when you hit a target.

Powers are checked every five ticks. Head-granted effects are removed when
you unequip or swap the head; existing potion and beacon effects are preserved.
Already-fired projectiles and debuffs on targets finish normally. Cooldowns
cannot be bypassed by swapping variants or respawning within a session.
Creeper blasts damage nearby living targets without damaging the wearer or
breaking blocks. Fire bolts and other magic attacks are aimed strikes that
do not create terrain-destroying fireballs. Teleporting requires an empty
destination with ground underneath and stops at obstacles.

These are playable adaptations of mob traits, not a full transformation into
the mob. For mobs without a useful player equivalent, the head grants a
related trait such as resistance, haste or regeneration. See the
[complete ability list](docs/head-abilities.md) for every head.

When updating from an older release, import the new `.mcaddon` and ensure the
world uses both **1.2.0** packs.

## Commands (cheats on)

- `/scriptevent mh:ledger` opens the Trophy Ledger.
- `/scriptevent mh:reset` clears your collection (handy for testing).

## Settings

Near the top of `src/scripts/main.js`:

- `DROP_CHANCE`: chance a head drops (default `1.0`, so always).
- `BOSS_PLAYER_RADIUS`, `CREAKING_RADIUS`: how close a player must be.

## Editing the heads

The packs are generated from Python, so tweaking a head means editing data, not
JSON.

- `tools/mobs.py` holds the data model and explains how art maps onto each
  face. Variants are listed with `V(...)`, including how the game tells them
  apart (the mob's `variant`, `mark_variant` or `color` component, or an entity
  property such as `minecraft:climate_variant`).
- `tools/art/*.py` hold the heads themselves: size, palette, pixel art for the
  front, sides, top and back, and extra cubes (snouts, ears, horns, hats).
- `tools/build.py` turns that into blocks, wearable items, block and worn
  geometry, attachables, textures, the language file, `scripts/heads.js` and the
  `.mcaddon`.
- `tools/preview.py` renders `docs/heads_preview.png` and
  `docs/worn_preview.png` from the generated geometry and textures, so you can
  check your art without launching the game.

```sh
pip install pillow
python3 tools/build.py
python3 tools/preview.py
python3 tools/preview.py --only cat --back --zoom 2 --out cats.png   # one mob, front and back
python3 tools/preview.py --only cat --worn --out cats_worn.png       # worn by a player
```

The build output all goes into `dist/`, which is wiped and recreated on every
build. The game script is hand written in `src/scripts/main.js` and copied into
the behavior pack, so edit it there, never in `dist/`.

If a future update adds a new mob, add an entry to one of the `tools/art/`
files and rebuild. The ledger and collection total update automatically.

## Project layout

```
src/scripts/main.js        game logic (hand written)
src/scripts/abilities.js   worn-head powers and ability descriptions
tests/abilities.test.cjs   ability lifecycle and combat regression tests
tools/                     generator and preview renderer
  art/                     head art, one file per group of mobs
dist/                      build output (generated, do not edit)
  MobTrophies_BP/          behavior pack (blocks, head items, ledger, recipe, scripts)
  MobTrophies_RP/          resource pack (geometry, attachables, textures, names)
  MobTrophies.mcaddon      both packs zipped, ready to install
```

## Validation

After rebuilding, run the behaviour tests:

```sh
node --test tests/abilities.test.cjs
```

To check the new power script against the exact stable Bedrock 2.0.0 API:

```sh
npm install
npm run check
```

The tests use a mocked Bedrock API to check all 205 heads, equipping and
removal, potion preservation, variants, cooldowns, multiplayer isolation,
teleport destinations, melee traits and projectile ownership. They do not
replace testing in Minecraft. For a manual smoke test, equip a Spider, Bat,
Enderman, Creeper, Bogged and aquatic head; try their controls, switch heads
and remove them, then repeat with a second player.

