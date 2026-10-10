# Agent instructions

This repo is the Mob Trophies add-on for Minecraft Bedrock. The add-on is
built into the `dist/` folder by `tools/build.py`: the behavior pack
(`dist/MobTrophies_BP/`), the resource pack (`dist/MobTrophies_RP/`) and the
installable `dist/MobTrophies.mcaddon`. Read `README.md` for the full layout.

## Always rebuild after changing the add-on

After **any** change that affects the add-on, rebuild before you finish or
commit:

```sh
python3 tools/build.py
```

This counts as a change to the add-on:

- `tools/mobs.py` (data model, helpers, vanilla heads, mob list)
- `tools/art/*.py` (head art, sizes, palettes, extra cubes, variants)
- `tools/build.py` (block, geometry, texture, manifest or packaging logic)
- `src/scripts/main.js` (the hand-written game script; the build copies it
  into `dist/`, so the packs and `.mcaddon` are stale until you rebuild)

The build must finish without errors. It validates the art and checks that
every head fits inside its block. If it fails, fix the cause and run it again.
Never hand-edit generated files to get around a failure.

If you changed head art, models or textures, also refresh the preview and
look at it to check the result:

```sh
python3 tools/preview.py   # writes docs/heads_preview.png, worn_preview.png, abilities_*.png
```

Then commit the regenerated files together with your source change,
including everything in `dist/` and (if refreshed) the images in `docs/`.
If you changed a head's powers in `src/scripts/abilities.js`, refresh the
ability cards too (`python3 tools/preview.py --abilities`).
The `.mcaddon` is committed on purpose so it can be downloaded straight from
GitHub onto a phone or tablet.

## Do not edit generated files

`dist/` is deleted and recreated on every build, so any edit made there is
lost. Make changes in `tools/mobs.py`, `tools/art/`, `tools/build.py` or
`src/scripts/main.js` instead.

## Setup

The build needs Python 3 and Pillow (`pip install pillow`).
