import { world, system, EquipmentSlot, Player, EntityDamageCause, InputButton, ButtonState } from "@minecraft/server";

/**
 * @typedef {{ id: string, amplifier: number }} PassiveEffect
 * @typedef {{ effect?: string, duration?: number, fire?: number, knockback?: number }} HitTrait
 * @typedef {object} HeadProfile
 * @property {string} description
 * @property {PassiveEffect[]} effects
 * @property {boolean} [fly]
 * @property {boolean} [swim]
 * @property {number} [swimSpeed]
 * @property {boolean} [climb]
 * @property {boolean} [shell]
 * @property {boolean} [hide]
 * @property {string} [action]
 * @property {string} [projectile]
 * @property {number} [damage]
 * @property {number} [cooldown]
 * @property {number} [distance]
 * @property {number} [range]
 * @property {boolean} [throughWalls]
 * @property {HitTrait} [hit]
 * @property {HitTrait} [melee]
 * @typedef {{ trail: string, impact?: string, sound: string, step?: number }} BeamFx
 * @typedef {{ key: string | undefined, effects: Map<string, { amplifier: number, until: number }>,
 *   cooldowns: Map<string, number>, sneaking: boolean, wasSneaking: boolean, sneakTick: number,
 *   readyAt?: number }} AbilityState
 * @typedef {import("@minecraft/server").Entity} Entity
 * @typedef {import("@minecraft/server").Vector3} Vector3
 */

// Amplifiers are zero based. These are playable adaptations of mob traits,
// rather than changes to the player's entity type or game mode.
/** @param {string} id */
const E = (id, amplifier = 0) => ({ id, amplifier });
const speed = E("speed"), strength = E("strength"), armour = E("resistance");
const jump = E("jump_boost"), night = E("night_vision"), fire = E("fire_resistance");
const regen = E("regeneration"), haste = E("haste"), glide = E("slow_falling");
const water = [E("water_breathing"), E("conduit_power")];
/** @param {string} description @param {PassiveEffect[]} effects
 * @param {Partial<HeadProfile>} extra @returns {HeadProfile} */
const P = (description, effects = [], extra = {}) => ({ description, effects, ...extra });
const fly = { fly: true };
const swim = { swim: true };
/** @param {string} projectile @param {number} damage @param {number} cooldown @param {HitTrait} [hit] */
const shot = (projectile, damage, cooldown, hit) => ({ action: "shot", projectile, damage, cooldown, hit });
/** @param {number} damage @param {number} range @param {number} cooldown @param {HitTrait} [hit] */
const ray = (damage, range, cooldown, hit) => ({ action: "ray", damage, range, cooldown, hit });
const poison = { effect: "poison", duration: 80 };
const wither = { effect: "wither", duration: 80 };
const chill = { effect: "slowness", duration: 100 };
const burn = { fire: 4 };
const knock = { knockback: 1.2 };

/** @type {Record<string, HeadProfile>} */
export const ABILITIES = {
  creeper: P("Crouch: blast nearby mobs (8s cooldown, no broken blocks).", [armour], { action: "blast", cooldown: 160 }),
  zombie: P("Strength and night vision.", [strength, night]),
  skeleton: P("Night vision. Crouch: shoot an arrow (2s).", [night], shot("minecraft:arrow", 4, 40)),
  wither_skeleton: P("Fire resistance; melee hits inflict Wither.", [fire, strength], { melee: wither }),
  piglin: P("Speed and strength.", [speed, strength]),
  ender_dragon: P("Flight and Strength II. Crouch: dragon breath (5s).", [E("strength", 1), glide], { ...fly, ...ray(10, 20, 100, { effect: "weakness", duration: 100 }) }),
  allay: P("Flight. Crouch: collect nearby drops matching your held item (2s).", [glide], { ...fly, action: "collect", cooldown: 40 }),
  armadillo: P("Resistance; crouching strengthens your protective shell.", [armour], { shell: true }),
  axolotl: P("Underwater breathing, swimming boost and regeneration.", [...water, regen], swim),
  bat: P("Flight and night vision.", [glide, night], fly),
  camel: P("Speed and high jumps. Crouch: forward dash (3s).", [speed, jump], { action: "dash", cooldown: 60 }),
  cat: P("Speed, night vision and gentle landings.", [speed, night, glide]),
  chicken: P("Flutter down slowly and jump higher.", [glide, jump]),
  cod: P("Underwater breathing and swimming boost.", water, swim),
  copper_golem: P("Resistance and faster mining.", [armour, haste]),
  cow: P("Resistance. Crouch: milk cleanse removes Poison and Wither (10s).", [armour], { action: "cleanse", cooldown: 200 }),
  donkey: P("Speed and resistance.", [speed, armour]),
  frog: P("Jump Boost III and underwater breathing.", [E("jump_boost", 2), E("water_breathing")]),
  glow_squid: P("Underwater breathing, night vision and swimming boost.", [...water, night], swim),
  happy_ghast: P("Flight and gentle landings.", [glide], fly),
  horse: P("Speed II and Jump Boost II.", [E("speed", 1), E("jump_boost", 1)]),
  mooshroom: P("Regeneration. Crouch: milk cleanse (10s).", [regen], { action: "cleanse", cooldown: 200 }),
  mule: P("Speed and faster mining.", [speed, haste]),
  skeleton_horse: P("Speed II, high jumps and underwater breathing.", [E("speed", 1), jump, E("water_breathing")]),
  zombie_horse: P("Speed II, high jumps and night vision.", [E("speed", 1), jump, night]),
  nautilus: P("Underwater breathing, resistance and swimming boost.", [...water, armour], swim),
  ocelot: P("Speed II, night vision and gentle landings.", [E("speed", 1), night, glide]),
  parrot: P("Flight and gentle landings.", [glide], fly),
  pig: P("Speed and resistance.", [speed, armour]),
  rabbit: P("Speed and Jump Boost III.", [speed, E("jump_boost", 2)]),
  salmon: P("Underwater breathing and swimming boost.", water, swim),
  sheep: P("Soft landings and regeneration.", [glide, regen]),
  sniffer: P("Faster digging. Crouch: collect nearby seed drops (3s).", [haste], { action: "seeds", cooldown: 60 }),
  snow_golem: P("Crouch: throw a chilling snowball (1s).", [], shot("minecraft:snowball", 2, 20, chill)),
  squid: P("Underwater breathing and swimming boost.", water, swim),
  strider: P("Fire resistance and speed.", [fire, speed]),
  tadpole: P("Underwater breathing and swimming boost.", water, swim),
  tropicalfish: P("Underwater breathing and swimming boost.", water, swim),
  turtle: P("Underwater breathing, resistance and swimming boost.", [...water, armour], swim),
  villager: P("Village trading discounts.", [E("village_hero")]),
  wandering_trader: P("Village trading discounts; crouch to become invisible.", [E("village_hero")], { hide: true }),
  sulfur_cube: P("High jumps and fire resistance (experimental bonus).", [E("jump_boost", 1), fire]),
  bee: P("Flight; melee hits poison targets.", [glide], { ...fly, melee: poison }),
  dolphin: P("Underwater breathing and a fast swimming boost.", water, { swim: true, swimSpeed: 0.8 }),
  enderman: P("Night vision. Crouch: teleport up to 12 blocks ahead (4s).", [night], { action: "teleport", cooldown: 80 }),
  fox: P("Speed II, Jump Boost II and night vision.", [E("speed", 1), E("jump_boost", 1), night]),
  goat: P("Jump Boost III; melee hits knock targets back.", [E("jump_boost", 2)], { melee: knock }),
  iron_golem: P("Strength II, Resistance II; melee hits launch targets.", [E("strength", 1), E("resistance", 1)], { melee: knock }),
  llama: P("Resistance. Crouch: spit at a target (2s).", [armour], ray(3, 16, 40)),
  trader_llama: P("Resistance. Crouch: spit at a target (2s).", [armour], ray(3, 16, 40)),
  panda: P("Strength and resistance.", [strength, armour]),
  polar_bear: P("Strength II and underwater breathing.", [E("strength", 1), E("water_breathing")]),
  pufferfish: P("Underwater breathing; melee hits poison targets.", water, { ...swim, melee: poison }),
  wolf: P("Speed and strength.", [speed, strength]),
  zombie_pigman: P("Fire resistance and strength.", [fire, strength]),
  blaze: P("Flight and fire resistance. Crouch: fire bolt (2s).", [fire, glide], { ...fly, ...ray(6, 24, 40, burn) }),
  bogged: P("Night vision. Crouch: poison arrow (3s).", [night], shot("minecraft:arrow", 4, 60, poison)),
  breeze: P("High jumps and gentle landings. Crouch: wind burst (3s).", [E("jump_boost", 2), glide], ray(4, 20, 60, knock)),
  camel_husk: P("Speed and high jumps; melee hits cause Hunger.", [speed, jump], { melee: { effect: "hunger", duration: 100 } }),
  cave_spider: P("Night vision; hold Jump against a wall to climb. Melee poisons.", [night], { climb: true, melee: poison }),
  creaking: P("Resistance III while crouching, plus night vision.", [night, armour], { shell: true }),
  drowned: P("Underwater breathing, strength and swimming boost.", [...water, strength], swim),
  elder_guardian: P("Underwater breathing and resistance. Crouch: fatigue beam (5s).", [...water, armour], { ...swim, ...ray(8, 20, 100, { effect: "mining_fatigue", duration: 100 }) }),
  endermite: P("Speed and night vision. Crouch: short teleport (4s).", [speed, night], { action: "teleport", distance: 6, cooldown: 80 }),
  evoker: P("Crouch: fang strike at the mob you look at (4s).", [armour], ray(8, 16, 80)),
  ghast: P("Flight and fire resistance. Crouch: fiery blast (4s).", [fire, glide], { ...fly, ...ray(8, 24, 80, burn) }),
  guardian: P("Underwater breathing. Crouch: guardian beam (3s).", water, { ...swim, ...ray(6, 20, 60) }),
  hoglin: P("Strength; melee hits knock targets back.", [strength], { melee: knock }),
  husk: P("Strength; melee hits cause Hunger.", [strength], { melee: { effect: "hunger", duration: 100 } }),
  magma_cube: P("Fire resistance and Jump Boost III; melee ignites targets.", [fire, E("jump_boost", 2)], { melee: burn }),
  parched: P("Night vision. Crouch: weakness arrow (3s).", [night], shot("minecraft:arrow", 4, 60, { effect: "weakness", duration: 100 })),
  phantom: P("Flight and night vision.", [glide, night], fly),
  piglin_brute: P("Strength II and resistance.", [E("strength", 1), armour]),
  pillager: P("Crouch: shoot a powerful arrow (2s).", [], shot("minecraft:arrow", 6, 40)),
  vindicator: P("Strength II and speed.", [E("strength", 1), speed]),
  ravager: P("Strength II, Resistance II; melee hits knock targets back.", [E("strength", 1), E("resistance", 1)], { melee: knock }),
  shulker: P("Resistance; crouch: levitation bolt (4s).", [E("resistance", 1)], ray(4, 20, 80, { effect: "levitation", duration: 60 })),
  silverfish: P("Speed and Haste II.", [speed, E("haste", 1)]),
  slime: P("Jump Boost III and soft landings.", [E("jump_boost", 2), glide]),
  spider: P("Night vision; hold Jump against a wall to climb.", [night], { climb: true }),
  stray: P("Night vision. Crouch: chilling arrow (3s).", [night], shot("minecraft:arrow", 4, 60, chill)),
  vex: P("Flight and strength.", [glide, strength], fly),
  warden: P("Strength III, Resistance II; crouch: sonic beam through walls (6s).", [E("strength", 2), E("resistance", 1)], { ...ray(12, 20, 120), throughWalls: true }),
  witch: P("Fire resistance and regeneration; melee hits poison targets.", [fire, regen], { melee: poison }),
  zoglin: P("Strength; melee hits knock targets back.", [strength], { melee: knock }),
  zombie_nautilus: P("Underwater breathing, night vision and swimming boost.", [...water, night], swim),
  zombie_villager: P("Strength and night vision.", [strength, night]),
  wither: P("Flight, fire resistance and regeneration. Crouch: Wither bolt (4s).", [fire, regen, glide], { ...fly, ...ray(8, 24, 80, wither) }),
};

// Each aimed power gets a visible beam and its mob's sound, so it is clear the
// power fired even when nothing is hit. Unlisted heads use DEFAULT_BEAM.
/** @type {BeamFx} */
const DEFAULT_BEAM = { trail: "minecraft:critical_hit_emitter", sound: "random.bow" };
/** @type {Record<string, BeamFx>} */
const BEAMS = {
  warden: { trail: "minecraft:sonic_explosion", sound: "mob.warden.sonic_boom", step: 1.5 },
  ender_dragon: { trail: "minecraft:dragon_breath_trail", sound: "mob.enderdragon.growl" },
  blaze: { trail: "minecraft:basic_flame_particle", sound: "mob.blaze.shoot" },
  ghast: { trail: "minecraft:basic_flame_particle", impact: "minecraft:large_explosion", sound: "mob.ghast.fireball" },
  wither: { trail: "minecraft:basic_smoke_particle", impact: "minecraft:large_explosion", sound: "mob.wither.shoot" },
  breeze: { trail: "minecraft:basic_smoke_particle", impact: "minecraft:wind_explosion_emitter", sound: "mob.breeze.shoot" },
  evoker: { trail: "minecraft:evoker_spell", sound: "mob.evocation_illager.cast_spell" },
  guardian: { trail: "minecraft:basic_bubble_particle", sound: "mob.guardian.attack" },
  elder_guardian: { trail: "minecraft:basic_bubble_particle", sound: "mob.elderguardian.curse" },
  shulker: { trail: "minecraft:end_rod", sound: "mob.shulker.shoot" },
  llama: { trail: "minecraft:basic_smoke_particle", sound: "mob.llama.spit" },
  trader_llama: { trail: "minecraft:basic_smoke_particle", sound: "mob.llama.spit" },
};

/** @param {string} key */
export function abilityDescription(key) {
  const profile = ABILITIES[key];
  return profile ? profile.description + (profile.fly ? " Hold Jump to rise; crouch to descend." : "") : "No head ability.";
}

const CHECK_INTERVAL = 5;
const EFFECT_TICKS = 80;
// Aim assist: aimed powers also lock on to a mob within this angle of the
// screen centre (or this many blocks of the aim line). Touch players tap a mob
// to attack it instead of centring it, so an exact ray rarely hits on a tablet.
const ASSIST_ANGLE = 20 * Math.PI / 180;
const ASSIST_SLACK = 1.5;
// The last mob a player hit stays a fallback target for this long.
const RECENT_HIT_TICKS = 200;
// Cooldowns at least this long announce when the power is ready again.
const READY_NOTICE = 60;
/** @type {Map<string, AbilityState>} */
const states = new Map();
/** @type {Map<string, { player: Player, profile: HeadProfile }>} */
const projectiles = new Map();
/** @type {Map<string, { entity: Entity, tick: number }>} */
const recentHits = new Map();
const SEEDS = new Set(["minecraft:wheat_seeds", "minecraft:melon_seeds", "minecraft:pumpkin_seeds",
  "minecraft:beetroot_seeds", "minecraft:torchflower_seeds", "minecraft:pitcher_pod"]);

/** @param {Player} player @param {Map<string, {mob: {key: string}}>} headByItem */
function wornProfile(player, headByItem) {
  const item = player.getComponent("minecraft:equippable")?.getEquipment(EquipmentSlot.Head);
  const entry = item && headByItem.get(item.typeId);
  return entry && { key: entry.mob.key, profile: ABILITIES[entry.mob.key] };
}

// Only remove effects we granted. Potions/beacons already active are left
// untouched; a stronger or newly extended effect relinquishes our ownership.
/** @param {import("@minecraft/server").Effect | undefined} effect
 * @param {{ amplifier: number, until: number }} lease @param {number} now */
function owned(effect, lease, now) {
  return effect && effect.amplifier === lease.amplifier &&
    Math.abs(effect.duration - Math.max(0, lease.until - now)) <= 2;
}

/** @param {Player} player @param {AbilityState} state @param {PassiveEffect[]} wanted @param {number} now */
function syncEffects(player, state, wanted, now) {
  const desired = new Map(wanted.map((effect) => [effect.id, effect]));
  for (const [id, lease] of state.effects) {
    const current = player.getEffect(id);
    if (!owned(current, lease, now)) {
      state.effects.delete(id);
    } else if (desired.get(id)?.amplifier !== lease.amplifier) {
      player.removeEffect(id);
      state.effects.delete(id);
    }
  }
  for (const effect of wanted) {
    const current = player.getEffect(effect.id);
    const lease = state.effects.get(effect.id);
    if (current && !lease) continue;
    if (current && current.duration > 20) continue;
    // A longer night-vision lease avoids the vanilla end-of-effect flicker.
    const duration = effect.id === "night_vision" ? 300 : EFFECT_TICKS;
    player.addEffect(effect.id, duration, { amplifier: effect.amplifier, showParticles: false });
    state.effects.set(effect.id, { amplifier: effect.amplifier, until: now + duration });
  }
}

/** @param {Vector3} a @param {Vector3} b */
const offset = (a, b) => ({ x: b.x - a.x, y: b.y - a.y, z: b.z - a.z });
/** @param {Vector3} v */
const length = (v) => Math.hypot(v.x, v.y, v.z);

/** Middle of a mob's body, between its feet and its eyes. @param {Entity} entity */
function centre(entity) {
  const feet = entity.location;
  let eyes = feet;
  try {
    eyes = entity.getHeadLocation();
  } catch {
    // Some entities have no head location; aim at their feet instead.
  }
  return { x: feet.x, y: (feet.y + eyes.y) / 2, z: feet.z };
}

/** @param {Player} player @param {Vector3} from @param {Vector3} to */
function inSight(player, from, to) {
  const path = offset(from, to);
  const distance = length(path);
  if (distance < 0.5) return true;
  const direction = { x: path.x / distance, y: path.y / distance, z: path.z / distance };
  return !player.dimension.getBlockFromRay(from, direction, { maxDistance: distance });
}

/** Mobs that aim assist may pick: not players, pets, armour stands or boats. @param {Player} player @param {Entity} entity */
function assistable(player, entity) {
  return entity.isValid && entity.id !== player.id && !!entity.getComponent("minecraft:health") &&
    !entity.getComponent("minecraft:is_tamed");
}

/**
 * The mob an aimed power hits: the one under the crosshair, else the mob
 * closest to the aim line within the assist cone, else the last mob the
 * player hit if it is still in range.
 * @param {Player} player @param {number} range @returns {Entity | undefined}
 */
function aimTarget(player, range, throughWalls = false) {
  const exact = player.getEntitiesFromViewDirection({ maxDistance: range, ignoreBlockCollision: throughWalls })
    .find((hit) => hit.entity.id !== player.id && hit.entity.getComponent("minecraft:health"));
  if (exact) return exact.entity;

  const eye = player.getHeadLocation();
  const view = player.getViewDirection();
  const candidates = [];
  const nearby = player.dimension.getEntities({ location: eye, maxDistance: range,
    excludeFamilies: ["player", "inanimate"], excludeTypes: ["minecraft:item", "minecraft:xp_orb"] });
  for (const entity of nearby) {
    if (!assistable(player, entity)) continue;
    const middle = centre(entity);
    const path = offset(eye, middle);
    const along = path.x * view.x + path.y * view.y + path.z * view.z;
    if (along <= 0) continue;
    const away = Math.sqrt(Math.max(0, length(path) ** 2 - along ** 2));
    if (away > ASSIST_SLACK && Math.atan2(away, along) > ASSIST_ANGLE) continue;
    candidates.push({ entity, middle, score: Math.atan2(away, along) + along * 0.002 });
  }
  candidates.sort((a, b) => a.score - b.score);
  for (const candidate of candidates) {
    if (throughWalls || inSight(player, eye, candidate.middle)) return candidate.entity;
  }

  const recent = recentHits.get(player.id);
  if (recent && system.currentTick - recent.tick <= RECENT_HIT_TICKS && recent.entity.isValid &&
      recent.entity.dimension.id === player.dimension.id) {
    const middle = centre(recent.entity);
    if (length(offset(eye, middle)) <= range && (throughWalls || inSight(player, eye, middle))) return recent.entity;
  }
  return undefined;
}

/** @param {Player} player @param {string} id @param {Vector3} location */
function particle(player, id, location) {
  try {
    player.dimension.spawnParticle(id, location);
  } catch {
    // A particle missing from an older game version is only cosmetic.
  }
}

/** @param {Player} player @param {string} id */
function sound(player, id) {
  try {
    player.dimension.playSound(id, player.location);
  } catch {
    // Same for sounds.
  }
}

/** Draw a beam from the wearer's eyes to `end`. @param {Player} player @param {BeamFx} fx @param {Vector3} end */
function beam(player, fx, end) {
  const start = player.getHeadLocation();
  const path = offset(start, end);
  const distance = length(path);
  const step = fx.step ?? 1;
  for (let travelled = step; travelled < distance; travelled += step) {
    const t = travelled / distance;
    particle(player, fx.trail, { x: start.x + path.x * t, y: start.y + path.y * t, z: start.z + path.z * t });
  }
  particle(player, fx.impact ?? fx.trail, end);
  sound(player, fx.sound);
}

/** Where a beam that hits nothing ends: the first block in view, or full range. @param {Player} player @param {number} range */
function beamEnd(player, range, throughWalls = false) {
  const eye = player.getHeadLocation();
  const view = player.getViewDirection();
  const block = throughWalls ? undefined : player.getBlockFromViewDirection({ maxDistance: range });
  const distance = block ? length(offset(eye, {
    x: block.block.location.x + block.faceLocation.x,
    y: block.block.location.y + block.faceLocation.y,
    z: block.block.location.z + block.faceLocation.z })) : range;
  return { x: eye.x + view.x * distance, y: eye.y + view.y * distance, z: eye.z + view.z * distance };
}

/**
 * Launch direction for a head projectile: towards the aim target, raised to
 * allow for the projectile's drop, or straight ahead with no target.
 * @param {Player} player @param {HeadProfile} profile @param {number} speed
 */
function launchDirection(player, profile, speed) {
  const target = aimTarget(player, 32);
  if (!target) return player.getViewDirection();
  const path = offset(player.getHeadLocation(), centre(target));
  const ticks = length(path) / speed;
  const gravity = profile.projectile === "minecraft:snowball" ? 0.03 : 0.05;
  path.y += 0.5 * gravity * ticks * ticks;
  const distance = length(path);
  return { x: path.x / distance, y: path.y / distance, z: path.z / distance };
}

/** @param {Player} player @param {import("@minecraft/server").Entity} target
 * @param {number} damage @param {HitTrait} hit */
function strike(player, target, damage, hit = {}) {
  if (damage) target.applyDamage(damage, { cause: EntityDamageCause.magic, damagingEntity: player });
  if (hit.effect) target.addEffect(hit.effect, hit.duration ?? 80, { amplifier: 0, showParticles: true });
  if (hit.fire) target.setOnFire(hit.fire, true);
  if (hit.knockback) {
    const direction = player.getViewDirection();
    target.applyKnockback({ x: direction.x * hit.knockback, z: direction.z * hit.knockback }, 0.4);
  }
}

/** @param {Player} player @param {number} range */
function teleportAhead(player, range) {
  const position = player.location;
  const direction = player.getViewDirection();
  // Stop at the first obstruction: do not tunnel through walls into unseen
  // rooms. Require clear feet/head blocks and solid, non-hazardous ground.
  const horizontal = Math.hypot(direction.x, direction.z);
  if (horizontal < 0.1) return false;
  const obstruction = player.dimension.getBlockFromRay(
    { x: position.x, y: position.y + 1, z: position.z },
    { x: direction.x / horizontal, y: 0, z: direction.z / horizontal },
    { maxDistance: range, includeLiquidBlocks: true });
  const max = obstruction ? Math.min(range, Math.hypot(
    obstruction.block.location.x + 0.5 - position.x,
    obstruction.block.location.z + 0.5 - position.z) - 1) : range;
  for (let distance = Math.floor(max); distance >= 2; distance--) {
    const x = position.x + direction.x / horizontal * distance;
    const z = position.z + direction.z / horizontal * distance;
    for (const offset of [0, 1, -1, 2, -2]) {
      const y = Math.floor(position.y) + offset;
      const feet = player.dimension.getBlock({ x: Math.floor(x), y, z: Math.floor(z) });
      const head = player.dimension.getBlock({ x: Math.floor(x), y: y + 1, z: Math.floor(z) });
      const below = player.dimension.getBlock({ x: Math.floor(x), y: y - 1, z: Math.floor(z) });
      if (!feet?.isAir || !head?.isAir || !below || below.isAir || below.isLiquid ||
          ["minecraft:magma", "minecraft:campfire", "minecraft:soul_campfire", "minecraft:cactus"].includes(below.typeId)) continue;
      // A collision ray distinguishes real ground from flowers/signs in 2.0,
      // where Block.isSolid is not available.
      const ground = player.dimension.getBlockFromRay(
        { x: Math.floor(x) + 0.5, y: y + 0.01, z: Math.floor(z) + 0.5 },
        { x: 0, y: -1, z: 0 }, { maxDistance: 1.2, includeLiquidBlocks: true });
      if (ground?.block.location.y !== y - 1) continue;
      if (player.tryTeleport({ x: Math.floor(x) + 0.5, y, z: Math.floor(z) + 0.5 }, { checkForBlocks: true })) return true;
    }
  }
  return false;
}

/** @param {Player} player @param {boolean} seeds */
function collectDrops(player, seeds) {
  const inventory = player.getComponent("minecraft:inventory")?.container;
  const held = inventory?.getItem(player.selectedSlotIndex);
  if (!inventory || (!seeds && !held)) return false;
  let collected = false;
  for (const entity of player.dimension.getEntities({ type: "minecraft:item", location: player.location, maxDistance: 6 })) {
    const stack = entity.getComponent("minecraft:item")?.itemStack;
    if (!stack || (seeds ? !SEEDS.has(stack.typeId) : stack.typeId !== held?.typeId)) continue;
    const remaining = inventory.addItem(stack);
    if (remaining?.amount === stack.amount) continue;
    entity.remove();
    if (remaining) player.dimension.spawnItem(remaining, player.location);
    collected = true;
  }
  return collected;
}

/** @param {Player} player @param {string} key @param {HeadProfile} profile */
function action(player, key, profile) {
  switch (profile.action) {
    case "teleport":
      if (!teleportAhead(player, profile.distance ?? 12)) return false;
      sound(player, "mob.endermen.portal");
      return true;
    case "cleanse":
      player.removeEffect("poison");
      player.removeEffect("wither");
      return true;
    case "collect":
    case "seeds":
      return collectDrops(player, profile.action === "seeds");
    case "dash": {
      const direction = player.getViewDirection();
      player.applyKnockback({ x: direction.x * 1.5, z: direction.z * 1.5 }, 0.25);
      return true;
    }
    case "blast":
      // Damage-only burst preserves builds and does not damage the wearer.
      particle(player, "minecraft:large_explosion", player.location);
      sound(player, "random.explode");
      for (const target of player.dimension.getEntities({ location: player.location, maxDistance: 5 })) {
        if (target.id === player.id || !target.getComponent("minecraft:health")) continue;
        strike(player, target, 10, knock);
      }
      return true;
    case "ray": {
      const range = profile.range ?? 16;
      const fx = BEAMS[key] ?? DEFAULT_BEAM;
      const target = aimTarget(player, range, profile.throughWalls);
      if (!target) {
        // Show the miss so the player knows the power works; no cooldown.
        beam(player, fx, beamEnd(player, range, profile.throughWalls));
        return false;
      }
      beam(player, fx, centre(target));
      strike(player, target, profile.damage ?? 0, profile.hit);
      return true;
    }
    case "shot": {
      if (!profile.projectile) return false;
      const direction = launchDirection(player, profile, 2);
      const origin = player.getHeadLocation();
      const entity = player.dimension.spawnEntity(profile.projectile, {
        x: origin.x + direction.x * 0.6, y: origin.y + direction.y * 0.6, z: origin.z + direction.z * 0.6,
      });
      const projectile = entity.getComponent("minecraft:projectile");
      if (!projectile) {
        entity.remove();
        return false;
      }
      projectile.owner = player;
      // Native arrows already inflict damage; apply only extra traits on hit.
      projectiles.set(entity.id, { player, profile });
      system.runTimeout(() => {
        projectiles.delete(entity.id);
        if (entity.isValid) entity.remove();
      }, 100);
      projectile.shoot({ x: direction.x * 2, y: direction.y * 2, z: direction.z * 2 });
      return true;
    }
    default:
      return false;
  }
}

/** @param {Player} player @param {HeadProfile} profile */
function move(player, profile) {
  if (profile.fly && player.isJumping && !player.isSneaking && !player.isFlying && !player.isGliding) {
    // Knockback works for players in the stable 2.0 API. A bounded vertical
    // impulse gives controlled ascent without switching to Creative mode.
    player.applyKnockback({ x: 0, z: 0 }, Math.max(0, 0.35 - player.getVelocity().y));
  }
  if (profile.climb && player.isJumping && !player.isSneaking) {
    const wall = player.getBlockFromViewDirection({ maxDistance: 1.2 });
    if (wall && !wall.block.isAir && !wall.block.isLiquid) {
      player.applyKnockback({ x: 0, z: 0 }, Math.max(0, 0.25 - player.getVelocity().y));
    }
  }
  if (profile.swim && player.isSwimming) {
    const direction = player.getViewDirection();
    const velocity = player.getVelocity();
    const maximum = profile.swimSpeed ?? 0.55;
    if (Math.hypot(velocity.x, velocity.z) < maximum) {
      player.applyKnockback({ x: direction.x * 0.08, z: direction.z * 0.08 }, 0);
    }
  }
}

/**
 * Use the worn head's special power, if it has one and it is off cooldown.
 * @param {Player} player @param {AbilityState} state @param {string} key @param {HeadProfile} profile
 */
function usePower(player, state, key, profile) {
  const now = system.currentTick;
  const ready = state.cooldowns.get(key) ?? 0;
  if (now < ready) {
    player.onScreenDisplay.setActionBar("§eHead power ready in " + Math.ceil((ready - now) / 20) + "s");
  } else if (action(player, key, profile)) {
    const cooldown = profile.cooldown ?? 20;
    state.cooldowns.set(key, now + cooldown);
    state.readyAt = cooldown >= READY_NOTICE ? now + cooldown : undefined;
  } else if (profile.action === "ray") {
    player.onScreenDisplay.setActionBar("§7Missed: no mob in range. Face a mob and crouch again.");
  } else {
    player.onScreenDisplay.setActionBar("§7No suitable target, drop or safe destination.");
  }
}

/** Record crouch changes every tick, remembering the state before the latest one. @param {Player} player @param {AbilityState} state */
function trackCrouch(player, state) {
  if (player.isSneaking === state.sneaking) return;
  state.wasSneaking = state.sneaking;
  state.sneaking = player.isSneaking;
  state.sneakTick = system.currentTick;
}

/** @param {Map<string, {mob: {key: string}}>} headByItem */
export function startHeadAbilities(headByItem) {
  // Crouch changes are tracked every tick so a press can tell whether the
  // player was standing just before it (see playerButtonInput below).
  system.runInterval(() => {
    for (const player of world.getAllPlayers()) {
      const state = states.get(player.id);
      if (!state) continue;
      try {
        trackCrouch(player, state);
      } catch (error) {
        console.warn("[Mob Trophies] Crouch tracking failed: " + error);
      }
    }
  }, 1);

  system.runInterval(() => {
    for (const player of world.getAllPlayers()) {
      try {
        const now = system.currentTick;
        const worn = wornProfile(player, headByItem);
        let state = states.get(player.id);
        if (!state) {
          state = { key: undefined, effects: new Map(), cooldowns: new Map(), sneaking: player.isSneaking,
            wasSneaking: player.isSneaking, sneakTick: now };
          states.set(player.id, state);
        }
        trackCrouch(player, state);
        const profile = worn?.profile;
        if (state.key !== worn?.key) {
          syncEffects(player, state, [], now);
          state.key = worn?.key;
          state.readyAt = undefined;
          if (profile) player.sendMessage("§6[Head power] §f" + abilityDescription(worn.key));
        }
        const wanted = profile ? [...profile.effects] : [];
        if (profile?.shell && player.isSneaking) {
          const index = wanted.findIndex((effect) => effect.id === "resistance");
          if (index >= 0) wanted.splice(index, 1);
          wanted.push(E("resistance", 2));
        }
        if (profile?.hide && player.isSneaking) wanted.push(E("invisibility"));
        syncEffects(player, state, wanted, now);
        if (profile) move(player, profile);
        if (state.readyAt !== undefined && now >= state.readyAt) {
          state.readyAt = undefined;
          if (profile?.action) player.onScreenDisplay.setActionBar("§aHead power ready");
        }
        if (!profile && state.effects.size === 0 && [...state.cooldowns.values()].every((until) => until <= now)) {
          states.delete(player.id);
        }
      } catch (error) {
        console.warn("[Mob Trophies] Head ability failed: " + error);
      }
    }
  }, CHECK_INTERVAL);

  world.afterEvents.entityHitEntity.subscribe((event) => {
    if (!(event.damagingEntity instanceof Player)) return;
    try {
      const player = event.damagingEntity;
      const profile = wornProfile(player, headByItem)?.profile;
      // A touch player taps the mob they fight, so it makes a good fallback target.
      recentHits.set(player.id, { entity: event.hitEntity, tick: system.currentTick });
      if (profile?.melee) strike(player, event.hitEntity, 0, profile.melee);
    } catch (error) {
      console.warn("[Mob Trophies] Head melee ability failed: " + error);
    }
  });

  // Special powers fire on the crouch button press itself, not by polling
  // isSneaking: on touch screens the press lasts a single tick and crouch is
  // usually a toggle, and underwater the button sinks rather than crouches.
  // A press that stands a toggle-crouching player back up is ignored.
  world.afterEvents.playerButtonInput.subscribe((event) => {
    if (event.button !== InputButton.Sneak || event.newButtonState !== ButtonState.Pressed) return;
    try {
      const player = event.player;
      const state = states.get(player.id);
      const worn = wornProfile(player, headByItem);
      // Wait until the main loop has registered a newly equipped head.
      if (!state || !worn?.profile?.action || state.key !== worn.key) return;
      const recentChange = system.currentTick - state.sneakTick <= 1;
      if (recentChange ? state.wasSneaking : state.sneaking) return;
      usePower(player, state, worn.key, worn.profile);
    } catch (error) {
      console.warn("[Mob Trophies] Head power failed: " + error);
    }
  }, { buttons: [InputButton.Sneak], state: ButtonState.Pressed });

  world.afterEvents.projectileHitEntity.subscribe((event) => {
    const shot = projectiles.get(event.projectile.id);
    if (!shot) return;
    projectiles.delete(event.projectile.id);
    try {
      const target = event.getEntityHit().entity;
      const { player, profile } = shot;
      if (player.isValid && target?.isValid) {
        // Snowballs normally do no damage; arrows keep their native damage.
        strike(player, target, profile.projectile === "minecraft:snowball" ? (profile.damage ?? 0) : Math.max(0, (profile.damage ?? 4) - 4), profile.hit);
      }
      system.run(() => { if (event.projectile.isValid) event.projectile.remove(); });
    } catch (error) {
      console.warn("[Mob Trophies] Head projectile ability failed: " + error);
    }
  });
  world.afterEvents.projectileHitBlock.subscribe((event) => {
    if (!projectiles.has(event.projectile.id)) return;
    projectiles.delete(event.projectile.id);
    system.run(() => { if (event.projectile.isValid) event.projectile.remove(); });
  });
  world.afterEvents.playerSpawn.subscribe((event) => {
    const state = states.get(event.player.id);
    if (!state) return;
    // Retain cooldowns through respawning, but discard dead effect leases.
    syncEffects(event.player, state, [], system.currentTick);
    state.key = undefined;
  });
  world.afterEvents.playerLeave.subscribe((event) => {
    states.delete(event.playerId);
    recentHits.delete(event.playerId);
  });
}
