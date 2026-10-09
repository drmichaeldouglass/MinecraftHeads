import { world, system, ItemStack, Player } from "@minecraft/server";
import { ActionFormData } from "@minecraft/server-ui";
import { HEADS } from "./heads.js";

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

const headByEntity = new Map();
const headByItem = new Map();
for (const head of HEADS) {
  for (const entityId of head.entities) headByEntity.set(entityId, head);
  headByItem.set(head.item, head);
}
const REQUIRED = HEADS.filter((h) => !h.experimental);
const BONUS = HEADS.filter((h) => h.experimental);
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

  const head = headByEntity.get(typeId);
  if (!head) return;

  const byPlayer = killingPlayer(event.damageSource) !== undefined;
  const bossCredit = BOSS_TYPES.has(typeId) && playerNearby(dimension, location, BOSS_PLAYER_RADIUS);
  if (!byPlayer && !bossCredit) return;
  if (Math.random() >= DROP_CHANCE) return;

  dropHead(head, dimension, location);
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

  const head = headByEntity.get("minecraft:creaking");
  if (!head || Math.random() >= DROP_CHANCE) return;
  // World changes are not allowed inside before-events, so drop it next tick.
  system.run(() => dropHead(head, dimension, location));
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

/** @param {Set<string>} set */
function requiredCount(set) {
  return REQUIRED.filter((h) => set.has(h.key)).length;
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
  const found = [];
  for (let slot = 0; slot < container.size; slot++) {
    const item = container.getItem(slot);
    if (!item) continue;
    const head = headByItem.get(item.typeId);
    if (head && !set.has(head.key)) {
      set.add(head.key);
      found.push(head);
    }
  }
  if (found.length === 0) return;

  saveCollection(player, set);
  for (const head of found) {
    const tag = head.experimental ? "§d(bonus)" : `§7(${requiredCount(set)}/${REQUIRED.length})`;
    player.sendMessage(`§6[Trophies] §fNew head collected: §e${head.name} ${tag}`);
  }
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

/** @param {{ key: string, name: string }[]} heads @param {Set<string>} set */
function listHeads(heads, set) {
  return heads
    .map((h) => (set.has(h.key) ? `§a[X] §f${h.name}` : `§8[ ] §7${h.name}`))
    .join("\n");
}

/** @param {Player} player */
function showLedger(player) {
  const set = getCollection(player);
  const done = requiredCount(set);
  const form = new ActionFormData()
    .title("Trophy Ledger")
    .body(
      `Collected §e${done}§r of §e${REQUIRED.length}§r mob heads\n` +
        `${progressBar(done, REQUIRED.length)}\n\n` +
        "Kill a mob to make it drop its head, then pick it up.\n" +
        "Place heads on the floor or on a wall to show them off!"
    );

  const pages = [];
  for (const category of CATEGORIES) {
    const heads = REQUIRED.filter((h) => h.category === category);
    if (heads.length === 0) continue;
    const have = heads.filter((h) => set.has(h.key)).length;
    form.button(`${category} mobs\n§8${have}/${heads.length}`);
    pages.push({ title: `${category} mobs`, heads });
  }
  if (BONUS.length > 0) {
    const have = BONUS.filter((h) => set.has(h.key)).length;
    form.button(`Bonus (experimental)\n§8${have}/${BONUS.length}`);
    pages.push({ title: "Bonus heads", heads: BONUS });
  }
  form.button("Close");

  form.show(player).then((response) => {
    if (response.canceled || response.selection === undefined) return;
    const page = pages[response.selection];
    if (!page) return;
    new ActionFormData()
      .title(page.title)
      .body(listHeads(page.heads, set))
      .button("Back")
      .show(player)
      .then((r) => {
        if (!r.canceled && r.selection === 0) showLedger(player);
      });
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
