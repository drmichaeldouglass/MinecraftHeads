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
  const intervals = [];
  const system = { currentTick: 0, runInterval(fn, period = 1) { intervals.push({ fn, period }); },
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
      this.dimension = { id: "overworld", spawnParticle() {}, playSound() {}, getEntities: () => [],
        getBlockFromRay: () => undefined,
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
    EntityDamageCause: { magic: "magic" }, InputButton: { Sneak: "Sneak", Jump: "Jump" },
    ButtonState: { Pressed: "Pressed", Released: "Released" }, console });
  vm.runInContext(code + "\nthis.api = { ABILITIES, abilityDescription, startHeadAbilities };", context);
  const lookup = new Map(MOBS.flatMap(m => m.heads.map(h => [h.item, { mob: m, head: h }])));
  context.api.startHeadAbilities(lookup);
  // Advance the game one tick at a time, running each interval on its period.
  function tick(count = 5) {
    for (let step = 0; step < count; step++) {
      system.currentTick++;
      for (const player of players) {
        for (const [id, effect] of player.effects) {
          effect.duration -= 1;
          if (effect.duration <= 0) player.effects.delete(id);
        }
      }
      for (const { fn, period } of intervals) {
        if (system.currentTick % period === 0) fn();
      }
    }
  }
  // Crouch button press. On touch screens isSneaking toggles, so a press can
  // also stand the player up; underwater it may not change at all.
  const press = (player, sneaking = true) => {
    player.isSneaking = sneaking;
    events.playerButtonInput({ player, button: "Sneak", newButtonState: "Pressed" });
  };
  const equip = (player, key, variant = 0) => { player.helmet = MOBS.find(m => m.key === key).heads[variant].item; };
  const target = (location = { x: 3, y: 64, z: 0 }, components = ["minecraft:health"]) => ({
    id: "target" + location.x + location.z, isValid: true, location, damage: [], effects: [],
    dimension: { id: "overworld" }, getHeadLocation: () => ({ ...location, y: location.y + 1.6 }),
    getComponent: id => components.includes(id) ? {} : undefined,
    applyDamage(amount, options) { this.damage.push({ amount, options }); },
    addEffect(...args) { this.effects.push(args); }, setOnFire() {}, applyKnockback() {} });
  return { api: context.api, Player, events, timers, tick, press, equip, target, players };
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

test("each crouch press fires once, cooldowns are per player, and swapping heads cannot reset them", () => {
  const { Player, equip, tick, press, target } = setup();
  const first = new Player("one"), second = new Player("two"), victim = target();
  first.hits = second.hits = [{ entity: victim }];
  equip(first, "blaze"); equip(second, "blaze"); tick();
  press(first); press(second);
  assert.equal(victim.damage.length, 2);
  tick(); assert.equal(victim.damage.length, 2);
  first.isSneaking = false; tick(); press(first);
  assert.equal(victim.damage.length, 2);
  assert.match(first.messages.at(-1), /ready in/);
  first.helmet = undefined; tick(); equip(first, "blaze"); tick();
  first.isSneaking = false; tick(); press(first);
  assert.equal(victim.damage.length, 2);
  first.isSneaking = false; tick(40); press(first);
  assert.equal(victim.damage.length, 3);
});

test("equipping while crouched does not fire; variant swaps share cooldowns", () => {
  const { Player, equip, tick, press } = setup();
  const player = new Player("one");
  player.isSneaking = true; equip(player, "cow"); tick();
  player.effects.set("poison", { amplifier: 0, duration: 100 });
  tick(); assert.ok(player.effects.has("poison"));
  press(player, false); tick(); assert.ok(player.effects.has("poison"));
  press(player); tick();
  assert.ok(!player.effects.has("poison"));
  equip(player, "cow", 1); tick(); player.effects.set("poison", { amplifier: 0, duration: 100 });
  player.isSneaking = false; tick(); press(player); tick();
  assert.ok(player.effects.has("poison"));
});

test("touch crouch toggles: standing back up does not fire, underwater presses do", () => {
  const { Player, equip, tick, press, target } = setup();
  const player = new Player("one"), victim = target();
  player.hits = [{ entity: victim }];
  equip(player, "warden"); tick();
  press(player); assert.equal(victim.damage.length, 1);
  tick(125);
  press(player, false); assert.equal(victim.damage.length, 1);
  tick(); press(player); assert.equal(victim.damage.length, 2);
  // Swimming: the button sinks the player and isSneaking stays false.
  player.isSneaking = false; tick(125);
  press(player, false); assert.equal(victim.damage.length, 3);
});

test("aim assist picks a mob near the crosshair, needs sight unless through walls, and skips pets", () => {
  const { Player, equip, tick, press, target } = setup();
  const player = new Player("one");
  const near = target({ x: 8, y: 64, z: 2 }), wide = target({ x: 8, y: 64, z: 6 });
  const pet = target({ x: 6, y: 64, z: 0.5 }, ["minecraft:health", "minecraft:is_tamed"]);
  player.dimension.getEntities = () => [wide, pet];
  equip(player, "blaze"); tick();
  press(player);
  assert.equal(wide.damage.length + pet.damage.length, 0);
  assert.match(player.messages.at(-1), /Missed/);
  // A miss starts no cooldown.
  player.dimension.getEntities = () => [wide, near, pet];
  player.isSneaking = false; tick(); press(player);
  assert.equal(near.damage.length, 1); assert.equal(wide.damage.length, 0);
  // Behind a wall: the blaze bolt is blocked but the warden beam goes through.
  player.dimension.getBlockFromRay = () => ({ block: { location: { x: 4, y: 65, z: 1 } } });
  player.isSneaking = false; tick(40); press(player);
  assert.equal(near.damage.length, 1);
  equip(player, "warden"); tick(); player.isSneaking = false; tick(); press(player);
  assert.equal(near.damage.length, 2);
});

test("aimed powers fall back to the last mob the player hit", () => {
  const { Player, equip, tick, press, target, events } = setup();
  const player = new Player("one"), behind = target({ x: -4, y: 64, z: 0 });
  equip(player, "evoker"); tick();
  events.entityHitEntity({ damagingEntity: player, hitEntity: behind });
  press(player);
  assert.equal(behind.damage.length, 1);
  behind.isValid = false; player.isSneaking = false; tick(80); press(player);
  assert.equal(behind.damage.length, 1);
});

test("head projectiles lead an assisted target and the ready notice follows long cooldowns", () => {
  const { Player, equip, tick, press, target } = setup();
  const player = new Player("one"), mob = target({ x: 16, y: 64, z: 4 });
  let component;
  player.dimension.spawnEntity = () => {
    component = { shoot(velocity) { this.velocity = velocity; } };
    return { id: "arrow", isValid: true, getComponent: () => component, remove() {} };
  };
  player.dimension.getEntities = () => [mob];
  equip(player, "bogged"); tick(); press(player);
  assert.ok(component.velocity.z > 0.3);
  assert.ok(component.velocity.y > 0);
  player.isSneaking = false; tick(55); assert.ok(!player.messages.includes("§aHead power ready"));
  tick(5); assert.ok(player.messages.includes("§aHead power ready"));
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
  const { Player, equip, tick, press, target } = setup();
  const player = new Player("one"), victim = target();
  player.dimension.getEntities = () => [player, victim];
  equip(player, "creeper"); tick(); press(player);
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
  const { Player, equip, tick, press } = setup();
  const player = new Player("one"); equip(player, "enderman"); tick();
  player.dimension.getBlockFromRay = (origin, direction) => direction.y === -1 ?
    { block: { location: { y: Math.floor(origin.y) - 1 } } } : undefined;
  press(player); assert.equal(player.destination.x, 12.5);
  player.destination = undefined;
  player.isSneaking = false; tick(80);
  player.dimension.getBlock = p => ({ isAir: p.y >= 64, isLiquid: p.y < 64, typeId: "minecraft:lava", location: p });
  press(player); assert.equal(player.destination, undefined);
});

test("head projectiles have player ownership, traits, and cleanup", () => {
  const { Player, equip, tick, press, target, events, timers } = setup();
  const player = new Player("one"), victim = target();
  let component, arrow;
  player.dimension.spawnEntity = () => {
    component = { shoot(velocity) { this.velocity = velocity; } };
    arrow = { id: "arrow", isValid: true, getComponent: () => component, remove() { this.isValid = false; } };
    return arrow;
  };
  equip(player, "bogged"); tick(); press(player);
  assert.equal(component.owner, player); assert.equal(component.velocity.x, 2);
  events.projectileHitEntity({ projectile: arrow, getEntityHit: () => ({ entity: victim }) });
  assert.equal(victim.effects[0][0], "poison");
  for (const fn of timers) fn();
  assert.equal(arrow.isValid, false);
});

test("respawn clears stale leases and retained cooldowns still block attacks", () => {
  const { Player, equip, tick, press, target, events } = setup();
  const player = new Player("one"), victim = target();
  player.hits = [{ entity: victim }]; equip(player, "blaze"); tick();
  press(player);
  events.playerSpawn({ player }); player.isSneaking = false; tick();
  press(player); assert.equal(victim.damage.length, 1);
});
