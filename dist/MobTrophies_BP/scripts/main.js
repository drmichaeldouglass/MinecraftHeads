import { world, system, EquipmentSlot, ItemStack, Player } from "@minecraft/server";
import { ActionFormData } from "@minecraft/server-ui";
import { MOBS } from "./heads.js";

// ---------------------------------------------------------------------------
// Settings
// ---------------------------------------------------------------------------

/** Chance (0 to 1) that a mob killed by a player drops its head. */
const DROP_CHANCE = 1.0;

/**
 * Bosses can die from things a player set up (end crystals, explosions) rather
 * than a direct hit. For these mobs a head still drops if a player is nearby.
 */
const BOSS_TYPES = new Set(["minecraft:ender_dragon", "minecraft:wither"]);
const BOSS_PLAYER_RADIUS = 96;

/** Creakings can only be beaten by breaking their heart block. */
const CREAKING_HEART = "minecraft:creaking_heart";
const CREAKING_RADIUS = 40;

/** How often (ticks) inventories are checked for newly collected heads. */
const SCAN_INTERVAL = 20;

const LEDGER_ID = "mh:trophy_ledger";
const PROP_COLLECTED = "mh:collected";
const PROP_LEDGER_GIVEN = "mh:ledger_given";
const PROP_COMPLETE = "mh:complete";

// ---------------------------------------------------------------------------
// Lookups
// ---------------------------------------------------------------------------

// Each mob has one or more heads: one per variant (cat breed, sheep colour,
// villager biome, ...). A mob counts as collected once any of them is.
const mobByEntity = new Map();
const headByItem = new Map();
for (const mob of MOBS) {
  for (const entityId of mob.entities) mobByEntity.set(entityId, mob);
  for (const head of mob.heads) headByItem.set(head.item, { mob, head });
}
const REQUIRED = MOBS.filter((m) => !m.experimental);
const BONUS = MOBS.filter((m) => m.experimental);
const ALL_HEADS = MOBS.flatMap((m) => m.heads);
const CATEGORIES = ["Passive", "Neutral", "Hostile", "Boss"];

// ---------------------------------------------------------------------------
// Head drops
// ---------------------------------------------------------------------------

/** @param {import("@minecraft/server").EntityDamageSource} source */
function killingPlayer(source) {
  const attacker = source.damagingEntity;
  return attacker instanceof Player ? attacker : undefined;
}

/**
 * @param {import("@minecraft/server").Dimension} dimension
 * @param {import("@minecraft/server").Vector3} location
 * @param {number} radius
 */
function playerNearby(dimension, location, radius) {
  return dimension.getPlayers({ location, maxDistance: radius }).length > 0;
}

/**
 * Read one of the things a head variant can be matched on.
 * @param {import("@minecraft/server").Entity} entity
 * @param {string} trait
 */
function readTrait(entity, trait) {
  try {
    switch (trait) {
      case "variant":
        return entity.getComponent("minecraft:variant")?.value;
      case "mark_variant":
        return entity.getComponent("minecraft:mark_variant")?.value;
      case "color":
        return entity.getComponent("minecraft:color")?.value;
      case "skin_id":
        return entity.getComponent("minecraft:skin_id")?.value;
      default:
        return entity.getProperty(trait); // e.g. minecraft:climate_variant
    }
  } catch {
    return undefined;
  }
}

/**
 * Pick the head that matches the mob's variant. Falls back to the first
 * (default) head if the variant is unknown, e.g. one added by a game update.
 * @param {{ heads: { match: Record<string, unknown> }[] }} mob
 * @param {import("@minecraft/server").Entity} entity
 */
function headFor(mob, entity) {
  if (mob.heads.length === 1) return mob.heads[0];
  const seen = new Map();
  const read = (trait) => {
    if (!seen.has(trait)) seen.set(trait, readTrait(entity, trait));
    return seen.get(trait);
  };
  for (const head of mob.heads) {
    const wanted = Object.entries(head.match);
    if (wanted.length > 0 && wanted.every(([trait, value]) => read(trait) === value)) return head;
  }
  return mob.heads[0];
}

/**
 * @param {{ item: string }} head
 * @param {import("@minecraft/server").Dimension} dimension
 * @param {import("@minecraft/server").Vector3} location
 */
function dropHead(head, dimension, location) {
  try {
    dimension.spawnItem(new ItemStack(head.item, 1), {
      x: location.x,
      y: location.y + 0.5,
      z: location.z,
    });
  } catch (error) {
    console.warn(`[Mob Trophies] Could not drop ${head.item}: ${error}`);
  }
}

world.afterEvents.entityDie.subscribe((event) => {
  const dead = event.deadEntity;
  let typeId, location, dimension;
  try {
    typeId = dead.typeId;
    location = dead.location;
    dimension = dead.dimension;
  } catch {
    return; // Entity already unloaded.
  }

  const mob = mobByEntity.get(typeId);
  if (!mob) return;

  const byPlayer = killingPlayer(event.damageSource) !== undefined;
  const bossCredit = BOSS_TYPES.has(typeId) && playerNearby(dimension, location, BOSS_PLAYER_RADIUS);
  if (!byPlayer && !bossCredit) return;
  if (Math.random() >= DROP_CHANCE) return;

  dropHead(headFor(mob, dead), dimension, location);
});

// Breaking an active creaking heart is how a player defeats a creaking.
world.beforeEvents.playerBreakBlock.subscribe((event) => {
  const block = event.block;
  if (block.typeId !== CREAKING_HEART) return;

  const location = block.center();
  const dimension = block.dimension;
  const creakings = dimension.getEntities({
    type: "minecraft:creaking",
    location,
    maxDistance: CREAKING_RADIUS,
  });
  if (creakings.length === 0) return;

  const mob = mobByEntity.get("minecraft:creaking");
  if (!mob || Math.random() >= DROP_CHANCE) return;
  // World changes are not allowed inside before-events, so drop it next tick.
  system.run(() => dropHead(mob.heads[0], dimension, location));
});

// ---------------------------------------------------------------------------
// Collection tracking
// ---------------------------------------------------------------------------

/** @type {Map<string, Set<string>>} */
const collectionCache = new Map();

/** @param {Player} player */
function getCollection(player) {
  let set = collectionCache.get(player.id);
  if (set) return set;
  set = new Set();
  const raw = player.getDynamicProperty(PROP_COLLECTED);
  if (typeof raw === "string") {
    try {
      for (const key of JSON.parse(raw)) set.add(key);
    } catch {
      console.warn(`[Mob Trophies] Ignoring corrupt collection data for ${player.name}`);
    }
  }
  collectionCache.set(player.id, set);
  return set;
}

/** @param {Player} player @param {Set<string>} set */
function saveCollection(player, set) {
  player.setDynamicProperty(PROP_COLLECTED, JSON.stringify([...set]));
}

/** @param {{ heads: { key: string }[] }} mob @param {Set<string>} set */
function hasMob(mob, set) {
  return mob.heads.some((h) => set.has(h.key));
}

/** @param {{ heads: { key: string }[] }} mob @param {Set<string>} set */
function headCount(mob, set) {
  return mob.heads.filter((h) => set.has(h.key)).length;
}

/** @param {Set<string>} set */
function requiredCount(set) {
  return REQUIRED.filter((m) => hasMob(m, set)).length;
}

/** @param {Set<string>} set */
function totalHeads(set) {
  return ALL_HEADS.filter((h) => set.has(h.key)).length;
}

/** @param {Player} player @param {Set<string>} set */
function celebrate(player, set) {
  if (player.getDynamicProperty(PROP_COMPLETE) === true) return;
  if (requiredCount(set) < REQUIRED.length) return;

  player.setDynamicProperty(PROP_COMPLETE, true);
  player.onScreenDisplay.setTitle("§6Trophy Master!", {
    subtitle: `All ${REQUIRED.length} mob heads collected`,
    fadeInDuration: 10,
    stayDuration: 100,
    fadeOutDuration: 20,
  });
  player.playSound("ui.toast.challenge_complete");
  world.sendMessage(`§6${player.name} has collected every mob head and is a Trophy Master!`);
}

/** @param {Player} player */
function scanInventory(player) {
  const container = player.getComponent("minecraft:inventory")?.container;
  if (!container) return;

  const set = getCollection(player);
  const items = [];
  for (let slot = 0; slot < container.size; slot++) {
    const item = container.getItem(slot);
    if (item) items.push(item);
  }
  // Heads worn in the helmet slot count too.
  const worn = player.getComponent("minecraft:equippable")?.getEquipment(EquipmentSlot.Head);
  if (worn) items.push(worn);

  let found = 0;
  for (const item of items) {
    const entry = headByItem.get(item.typeId);
    if (!entry || set.has(entry.head.key)) continue;
    const { mob, head } = entry;
    const newMob = !hasMob(mob, set);
    set.add(head.key);
    found++;
    let tag;
    if (mob.experimental) tag = "§d(bonus)";
    else if (newMob) tag = `§7(${requiredCount(set)}/${REQUIRED.length})`;
    else tag = `§7(${mob.name} variant ${headCount(mob, set)}/${mob.heads.length})`;
    const what = newMob ? "New head collected" : "New variant collected";
    player.sendMessage(`§6[Trophies] §f${what}: §e${head.name} ${tag}`);
  }
  if (found === 0) return;

  saveCollection(player, set);
  player.playSound("random.levelup", { pitch: 1.5, volume: 0.6 });
  celebrate(player, set);
}

system.runInterval(() => {
  for (const player of world.getAllPlayers()) {
    try {
      scanInventory(player);
    } catch (error) {
      console.warn(`[Mob Trophies] Inventory scan failed: ${error}`);
    }
  }
}, SCAN_INTERVAL);

world.afterEvents.playerLeave.subscribe((event) => {
  collectionCache.delete(event.playerId);
});

// ---------------------------------------------------------------------------
// Trophy Ledger
// ---------------------------------------------------------------------------

/** @param {number} done @param {number} total */
function progressBar(done, total) {
  const width = 20;
  const filled = Math.round((done / total) * width);
  return `§a${"|".repeat(filled)}§8${"|".repeat(width - filled)}§r`;
}

/** @param {boolean} have @param {string} text */
function tick(have, text) {
  return have ? `§a[X] §f${text}` : `§8[ ] §7${text}`;
}

/** @param {typeof MOBS} mobs @param {Set<string>} set */
function listMobs(mobs, set) {
  return mobs
    .map((m) => {
      const line = tick(hasMob(m, set), m.name);
      return m.heads.length > 1 ? `${line} §8(${headCount(m, set)}/${m.heads.length})` : line;
    })
    .join("\n");
}

/** @param {Player} player @param {(typeof MOBS)[number]} mob @param {() => void} back */
function showVariants(player, mob, back) {
  const set = getCollection(player);
  new ActionFormData()
    .title(`${mob.name} heads`)
    .body(
      `Collected §e${headCount(mob, set)}§r of §e${mob.heads.length}§r ${mob.name} heads\n\n` +
        mob.heads.map((h) => tick(set.has(h.key), h.name)).join("\n")
    )
    .button("Back")
    .show(player)
    .then((r) => {
      if (!r.canceled && r.selection === 0) back();
    });
}

/** @param {Player} player @param {string} title @param {typeof MOBS} mobs */
function showPage(player, title, mobs) {
  const set = getCollection(player);
  const withVariants = mobs.filter((m) => m.heads.length > 1);
  const form = new ActionFormData().title(title).body(listMobs(mobs, set));
  for (const mob of withVariants) {
    form.button(`${mob.name} variants\n§8${headCount(mob, set)}/${mob.heads.length}`);
  }
  form.button("Back");
  form.show(player).then((r) => {
    if (r.canceled || r.selection === undefined) return;
    const mob = withVariants[r.selection];
    if (mob) showVariants(player, mob, () => showPage(player, title, mobs));
    else showLedger(player);
  });
}

/** @param {Player} player */
function showLedger(player) {
  const set = getCollection(player);
  const done = requiredCount(set);
  const form = new ActionFormData()
    .title("Trophy Ledger")
    .body(
      `Collected §e${done}§r of §e${REQUIRED.length}§r mob heads\n` +
        `${progressBar(done, REQUIRED.length)}\n` +
        `Variants: §e${totalHeads(set)}§r of §e${ALL_HEADS.length}§r heads\n\n` +
        "Kill a mob to make it drop its head, then pick it up.\n" +
        "Many mobs have a different head for each variant: every cat breed, " +
        "sheep colour and villager biome.\n" +
        "Place heads on the floor or on a wall, or wear them as a helmet!"
    );

  const pages = [];
  for (const category of CATEGORIES) {
    const mobs = REQUIRED.filter((m) => m.category === category);
    if (mobs.length === 0) continue;
    const have = mobs.filter((m) => hasMob(m, set)).length;
    form.button(`${category} mobs\n§8${have}/${mobs.length}`);
    pages.push({ title: `${category} mobs`, mobs });
  }
  if (BONUS.length > 0) {
    const have = BONUS.filter((m) => hasMob(m, set)).length;
    form.button(`Bonus (experimental)\n§8${have}/${BONUS.length}`);
    pages.push({ title: "Bonus heads", mobs: BONUS });
  }
  form.button("Close");

  form.show(player).then((response) => {
    if (response.canceled || response.selection === undefined) return;
    const page = pages[response.selection];
    if (page) showPage(player, page.title, page.mobs);
  });
}

world.afterEvents.itemUse.subscribe((event) => {
  if (event.itemStack.typeId === LEDGER_ID) showLedger(event.source);
});

world.afterEvents.playerSpawn.subscribe((event) => {
  const player = event.player;
  if (!event.initialSpawn || player.getDynamicProperty(PROP_LEDGER_GIVEN) === true) return;
  const container = player.getComponent("minecraft:inventory")?.container;
  if (!container) return;
  container.addItem(new ItemStack(LEDGER_ID, 1));
  player.setDynamicProperty(PROP_LEDGER_GIVEN, true);
  player.sendMessage(
    "§6[Trophies] §fEvery mob now drops its head when you kill it. " +
      "Use your §eTrophy Ledger§f to track your collection!"
  );
});

// /scriptevent mh:ledger  opens the ledger for the player who runs it
// /scriptevent mh:reset   clears that player's collection (for testing)
system.afterEvents.scriptEventReceive.subscribe((event) => {
  const player = event.sourceEntity;
  if (!(player instanceof Player)) return;
  if (event.id === "mh:ledger") {
    showLedger(player);
  } else if (event.id === "mh:reset") {
    collectionCache.set(player.id, new Set());
    player.setDynamicProperty(PROP_COLLECTED, undefined);
    player.setDynamicProperty(PROP_COMPLETE, undefined);
    player.sendMessage("§6[Trophies] §fYour head collection has been reset.");
  }
});
