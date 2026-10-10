const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const code = fs.readFileSync(path.join(root, "src/scripts/abilities.js"), "utf8")
  .replace(/^import .*;\n/, "").replace(/export /g, "");
const data = fs.readFileSync(path.join(root, "dist/MobTrophies_BP/scripts/heads.js"), "utf8");
const MOBS = JSON.parse(data.slice(data.indexOf("= ") + 2).replace(/;\s*$/, ""));

function setup() {
  const events = {};
  const timers = [];
  const players = [];
  const system = { currentTick: 0, runInterval(fn) { this.update = fn; },
    run(fn) { timers.push(fn); }, runTimeout(fn) { timers.push(fn); } };
  const world = { getAllPlayers: () => players, afterEvents: new Proxy({}, {
    get: (_, name) => ({ subscribe: fn => events[name] = fn }),
  }) };
  class Player {
    constructor(id) {
      this.id = id; this.isValid = true; this.effects = new Map(); this.isSneaking = false;
      this.isJumping = false; this.isSwimming = false; this.selectedSlotIndex = 0;
      this.location = { x: 0, y: 64, z: 0 }; this.messages = []; this.impulses = [];
      this.onScreenDisplay = { setActionBar: text => this.messages.push(text) };
      this.dimension = { spawnParticle() {}, getEntities: () => [], getBlockFromRay: () => undefined,
        getBlock: p => ({ isAir: p.y >= 64, isLiquid: false, typeId: p.y >= 64 ? "minecraft:air" : "minecraft:stone", location: p }) };
      players.push(this);
    }
    getComponent(id) {
      if (id === "minecraft:equippable") return { getEquipment: () => this.helmet ? { typeId: this.helmet } : undefined };
    }
    getEffect(id) { return this.effects.get(id); }
    addEffect(id, duration, options) { this.effects.set(id, { duration, amplifier: options.amplifier }); }
    removeEffect(id) { this.effects.delete(id); }
    sendMessage(text) { this.messages.push(text); }
    getViewDirection() { return { x: 1, y: 0, z: 0 }; }
    getHeadLocation() { return { x: 0, y: 65.6, z: 0 }; }
    getVelocity() { return { x: 0, y: 0, z: 0 }; }
    getBlockFromViewDirection() { return this.wall; }
    getEntitiesFromViewDirection() { return this.hits ?? []; }
    applyKnockback(...args) { this.impulses.push(args); }
    tryTeleport(position) { this.destination = position; return true; }
  }
  const context = vm.createContext({ world, system, Player, EquipmentSlot: { Head: "Head" },
    EntityDamageCause: { magic: "magic" }, console });
  vm.runInContext(code + "\nthis.api = { ABILITIES, abilityDescription, startHeadAbilities };", context);
  const lookup = new Map(MOBS.flatMap(m => m.heads.map(h => [h.item, { mob: m, head: h }])));
  context.api.startHeadAbilities(lookup);
  function tick(count = 5) {
    system.currentTick += count;
    for (const player of players) {
      for (const [id, effect] of player.effects) {
        effect.duration -= count;
        if (effect.duration <= 0) player.effects.delete(id);
      }
    }
    system.update();
  }
  const equip = (player, key, variant = 0) => { player.helmet = MOBS.find(m => m.key === key).heads[variant].item; };
  const target = () => ({ id: "target", isValid: true, location: { x: 3, y: 64, z: 0 }, damage: [], effects: [],
    getComponent: id => id === "minecraft:health" ? {} : undefined,
    applyDamage(amount, options) { this.damage.push({ amount, options }); },
    addEffect(...args) { this.effects.push(args); }, setOnFire() {}, applyKnockback() {} });
  return { api: context.api, Player, events, timers, tick, equip, target, players };
}

test("every mob and all 205 heads resolve to a documented ability", () => {
  const { api, Player, equip, tick } = setup();
  assert.equal(MOBS.flatMap(m => m.heads).length, 205);
  for (const mob of MOBS) {
    assert.ok(api.ABILITIES[mob.key], mob.key);
    assert.notEqual(api.abilityDescription(mob.key), "No head ability.");
    for (let index = 0; index < mob.heads.length; index++) {
      const player = new Player(mob.key + index);
      equip(player, mob.key, index); tick();
      assert.ok(player.messages.some(text => text.includes(api.ABILITIES[mob.key].description)), mob.heads[index].item);
    }
  }
});

test("helmet powers clear on removal and switching; inventory heads grant nothing", () => {
  const { Player, equip, tick } = setup();
  const player = new Player("one"); tick();
  assert.equal(player.effects.size, 0);
  equip(player, "zombie"); tick();
  assert.ok(player.effects.has("strength")); assert.ok(player.effects.has("night_vision"));
  equip(player, "cod"); tick();
  assert.ok(player.effects.has("water_breathing")); assert.ok(!player.effects.has("strength"));
  player.helmet = undefined; tick();
  assert.equal(player.effects.size, 0);
});

test("existing potions and newly extended effects survive unequipping", () => {
  const { Player, equip, tick } = setup();
  const player = new Player("one");
  player.effects.set("strength", { amplifier: 2, duration: 1000 });
  equip(player, "zombie"); tick();
  assert.equal(player.effects.get("strength").amplifier, 2);
  player.effects.set("night_vision", { amplifier: 0, duration: 1000 });
  player.helmet = undefined; tick();
  assert.equal(player.effects.get("night_vision").duration, 995);
  assert.ok(player.effects.has("strength"));
});

test("shell strengthens while crouching and returns to normal when released", () => {
  const { Player, equip, tick } = setup();
  const player = new Player("one"); equip(player, "armadillo"); tick();
  assert.equal(player.effects.get("resistance").amplifier, 0);
  player.isSneaking = true; tick(); assert.equal(player.effects.get("resistance").amplifier, 2);
  player.isSneaking = false; tick(); assert.equal(player.effects.get("resistance").amplifier, 0);
});

test("active abilities require a new crouch, have independent cooldowns, and cannot be reset by swapping heads", () => {
  const { Player, equip, tick, target } = setup();
  const first = new Player("one"), second = new Player("two"), victim = target();
  first.hits = second.hits = [{ entity: victim }];
  equip(first, "blaze"); equip(second, "blaze"); tick();
  first.isSneaking = second.isSneaking = true; tick();
  assert.equal(victim.damage.length, 2);
  tick(); assert.equal(victim.damage.length, 2);
  first.isSneaking = false; tick(); first.isSneaking = true; tick();
  assert.equal(victim.damage.length, 2);
  first.helmet = undefined; tick(); equip(first, "blaze"); tick();
  first.isSneaking = false; tick(); first.isSneaking = true; tick();
  assert.equal(victim.damage.length, 2);
  first.isSneaking = false; tick(40); first.isSneaking = true; tick();
  assert.equal(victim.damage.length, 3);
});

test("equipping while crouched does not fire; variant swaps share cooldowns", () => {
  const { Player, equip, tick } = setup();
  const player = new Player("one");
  player.isSneaking = true; equip(player, "cow"); tick();
  player.effects.set("poison", { amplifier: 0, duration: 100 });
  tick(); assert.ok(player.effects.has("poison"));
  player.isSneaking = false; tick(); player.isSneaking = true; tick();
  assert.ok(!player.effects.has("poison"));
  equip(player, "cow", 1); tick(); player.effects.set("poison", { amplifier: 0, duration: 100 });
  player.isSneaking = false; tick(); player.isSneaking = true; tick();
  assert.ok(player.effects.has("poison"));
});

test("melee traits use the currently worn head", () => {
  const { Player, equip, events, target } = setup();
  const player = new Player("one"), victim = target(); equip(player, "cave_spider");
  events.entityHitEntity({ damagingEntity: player, hitEntity: victim });
  assert.equal(victim.effects[0][0], "poison");
  player.helmet = undefined;
  events.entityHitEntity({ damagingEntity: player, hitEntity: victim });
  assert.equal(victim.effects.length, 1);
});

test("Creeper burst damages nearby targets but excludes wearer and never changes blocks", () => {
  const { Player, equip, tick, target } = setup();
  const player = new Player("one"), victim = target();
  player.dimension.getEntities = () => [player, victim];
  equip(player, "creeper"); tick(); player.isSneaking = true; tick();
  assert.equal(victim.damage[0].amount, 10);
  assert.equal(victim.damage[0].options.damagingEntity, player);
});

test("flight and wall climbing stop when the head is removed", () => {
  const { Player, equip, tick } = setup();
  const player = new Player("one"); player.isJumping = true;
  equip(player, "bat"); tick(); assert.equal(player.impulses.length, 1);
  player.helmet = undefined; tick(); assert.equal(player.impulses.length, 1);
  equip(player, "spider"); player.wall = { block: { isAir: false, isLiquid: false } };
  tick(); assert.equal(player.impulses.length, 2);
});

test("teleport requires collision ground and avoids unsafe destinations", () => {
  const { Player, equip, tick } = setup();
  const player = new Player("one"); equip(player, "enderman"); tick();
  player.dimension.getBlockFromRay = (origin, direction) => direction.y === -1 ?
    { block: { location: { y: Math.floor(origin.y) - 1 } } } : undefined;
  player.isSneaking = true; tick(); assert.equal(player.destination.x, 12.5);
  player.destination = undefined;
  player.isSneaking = false; tick(80);
  player.dimension.getBlock = p => ({ isAir: p.y >= 64, isLiquid: p.y < 64, typeId: "minecraft:lava", location: p });
  player.isSneaking = true; tick(); assert.equal(player.destination, undefined);
});

test("head projectiles have player ownership, traits, and cleanup", () => {
  const { Player, equip, tick, target, events, timers } = setup();
  const player = new Player("one"), victim = target();
  let component, arrow;
  player.dimension.spawnEntity = () => {
    component = { shoot(velocity) { this.velocity = velocity; } };
    arrow = { id: "arrow", isValid: true, getComponent: () => component, remove() { this.isValid = false; } };
    return arrow;
  };
  equip(player, "bogged"); tick(); player.isSneaking = true; tick();
  assert.equal(component.owner, player); assert.equal(component.velocity.x, 2);
  events.projectileHitEntity({ projectile: arrow, getEntityHit: () => ({ entity: victim }) });
  assert.equal(victim.effects[0][0], "poison");
  for (const fn of timers) fn();
  assert.equal(arrow.isValid, false);
});

test("respawn clears stale leases and retained cooldowns still block attacks", () => {
  const { Player, equip, tick, target, events } = setup();
  const player = new Player("one"), victim = target();
  player.hits = [{ entity: victim }]; equip(player, "blaze"); tick();
  player.isSneaking = true; tick();
  events.playerSpawn({ player }); player.isSneaking = false; tick();
  player.isSneaking = true; tick(); assert.equal(victim.damage.length, 1);
});
