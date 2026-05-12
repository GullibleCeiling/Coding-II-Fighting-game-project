#THis is where the entire game when it is fully done is gonna go

import random
import time


# =========================
# BASE CHARACTER SYSTEM
# =========================

class Character:
    def __init__(self, name, health, art, description):
        self.name = name
        self.max_health = health
        self.health = health
        self.art = art
        self.description = description

        self.defending = False
        self.pending_actions = []  # for delayed moves (Mortar Brick, etc)
        self.meter = 0

    def is_alive(self):
        return self.health > 0

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.health = 0

    def hp_bar(self, length=20):
        ratio = self.health / self.max_health
        filled = int(ratio * length)
        return f"[{'█'*filled}{'░'*(length-filled)}] {self.health}/{self.max_health}"


# =========================
# CHARACTER IMPLEMENTATIONS
# =========================

class Feignaz(Character):
    def attack(self, other, move):
        if move == "grapple":
            dmg = 7
            other.take_damage(dmg)
            return f"🤼 Feignaz grapples for {dmg} damage!"
        elif move == "taunt":
            self.meter += 1
            return f"🤼 Feignaz taunts! (meter: {self.meter})"
        elif move == "punch":
            dmg = 5
            other.take_damage(dmg)
            return f"👊 Punch for {dmg}"


class Kazuki(Character):
    def attack(self, other, move):
        if move == "rush":
            dmg = random.randint(2, 10)
            other.take_damage(dmg)
            return f"⚡ Kazuki rushes for {dmg}!"
        elif move == "taunt":
            self.meter += 1
            return f"⚡ Kazuki taunts! (meter: {self.meter})"
        elif move == "punch":
            dmg = 5
            other.take_damage(dmg)
            return f"👊 Punch for {dmg}"


class BrickAndMortar(Character):
    def attack(self, other, move):
        if move == "brick":
            self.pending_actions.append({"turns": 2, "damage": 8, "target": other})
            return "🧱 Mortar launches Brick (hits in 2 turns!)"
        elif move == "taunt":
            self.meter += 1
            return f"🧱 Brick & Mortar taunt! (meter: {self.meter})"


class BurnableDan(Character):
    def attack(self, other, move):
        if move == "fireball":
            dmg = 3
            other.take_damage(dmg)
            return f"🔥 Fireball hits for {dmg}"
        elif move == "taunt":
            self.meter += 1
            return f"🔥 Burnable Dan taunts! (meter: {self.meter})"


class HughMann(Character):
    def attack(self, other, move):
        if move == "slashes":
            dmg = 6
            other.take_damage(dmg)
            return f"⚔️ Slashes for {dmg}"
        elif move == "bonk":
            self.pending_actions.append({"turns": 2, "hits": 3, "damage": 6, "target": other})
            return "🔨 Judgement Bonk incoming (3 hits, slow!)"
        elif move == "taunt":
            self.meter += 1
            return f"⚔️ Hugh-Mann taunts! (meter: {self.meter})"


class JohnCameraman(Character):
    def attack(self, other, move):
        if move == "camera":
            self.meter += 1
            dmg = self.meter
            other.take_damage(dmg)
            return f"📸 Camera hits for {dmg} (meter: {self.meter})"
        elif move == "taunt":
            self.meter += 1
            return f"📸 John Cameraman taunts! (meter: {self.meter})"


class PerryPenguin(Character):
    def attack(self, other, move):
        if move == "rush":
            self.pending_actions.append({"turns": 2, "damage": 8, "hits": 2, "target": other})
            return "🐧 Perry launches attack (delayed double hit!)"
        elif move == "taunt":
            self.meter += 1
            return f"🐧 Perry Penguin taunts! (meter: {self.meter})"


class Catscade(Character):
    def attack(self, other, move):
        if move == "avenge":
            self.next_bonus = self.max_health - self.health
            return f"😾 Catscade prepares Avenge! (bonus: +{self.next_bonus})"
        elif move == "hit":
            dmg = 6 + getattr(self, "next_bonus", 0)
            self.next_bonus = 0
            other.take_damage(dmg)
            return f"🐱 Hit for {dmg}"
        elif move == "taunt":
            self.meter += 1
            return f"😾 Catscade taunts! (meter: {self.meter})"


class BigKeyBoy(Character):
    def attack(self, other, move):
        if move == "crown":
            dmg = random.randint(4, 9)
            other.take_damage(dmg)
            return f"👑 Big Key Boy rushes for {dmg}"
        elif move == "taunt":
            self.meter += 1
            return f"👑 Big Key Boy taunts! (meter: {self.meter})"


class Incrediboy(Character):
    def attack(self, other, move):
        if move == "punch":
            dmg = 4
            other.take_damage(dmg)
            return f"💥 Incrediboy hits for {dmg}"
        elif move == "taunt":
            self.meter += 1
            return f"💥 Incrediboy taunts! (meter: {self.meter})"


# =========================
# GAME ENGINE
# =========================

class Game:
    def __init__(self, p1, p2):
        self.players = [p1, p2]
        self.turn = 0

    def current(self):
        return self.players[self.turn % 2]

    def other(self):
        return self.players[(self.turn + 1) % 2]

    def resolve_pending(self, player):
        new_queue = []
        for action in player.pending_actions:
            action["turns"] -= 1

            if action["turns"] <= 0:
                if "hits" in action:
                    for _ in range(action["hits"]):
                        action["target"].take_damage(action["damage"])
                    print(f"💥 Delayed multi-hit lands for {action['damage']} x{action['hits']}")
                else:
                    action["target"].take_damage(action["damage"])
                    print(f"💥 Delayed attack hits for {action['damage']}")
            else:
                new_queue.append(action)

        player.pending_actions = new_queue

    def take_turn(self):
        p = self.current()
        o = self.other()

        self.resolve_pending(p)

        print(f"\n{p.name}'s turn")
        print("1 Punch | 2 Taunt | 3 Special")

        move = input("Move: ")

        if isinstance(p, Feignaz):
            action = "grapple" if move == "3" else "taunt" if move == "2" else "punch"
        elif isinstance(p, Kazuki):
            action = "rush" if move == "3" else "taunt" if move == "2" else "punch"
        elif isinstance(p, BrickAndMortar):
            action = "brick" if move == "3" else "taunt"
        elif isinstance(p, BurnableDan):
            action = "fireball" if move == "3" else "taunt"
        elif isinstance(p, HughMann):
            action = "bonk" if move == "3" else "taunt" if move == "2" else "slashes"
        elif isinstance(p, JohnCameraman):
            action = "camera" if move == "3" else "taunt"
        elif isinstance(p, PerryPenguin):
            action = "rush" if move == "3" else "taunt"
        elif isinstance(p, Catscade):
            action = "avenge" if move == "3" else "taunt" if move == "2" else "hit"
        elif isinstance(p, BigKeyBoy):
            action = "crown" if move == "3" else "taunt"
        else:
            action = "taunt" if move == "2" else "punch"

        print(p.attack(o, action))

        self.turn += 1

    def is_over(self):
        return any(not p.is_alive() for p in self.players)

    def winner(self):
        alive = [p for p in self.players if p.is_alive()]
        return alive[0].name if alive else "None"

    def status(self):
        for p in self.players:
            print(f"{p.name}: {p.hp_bar()}")


# =========================
# CHARACTER SELECT
# =========================

roster = {
    "1": Feignaz("Feignaz", 75, "", "Grappler"),
    "2": Kazuki("Kazuki", 75, "", "Rushdown"),
    "3": BrickAndMortar("Brick & Mortar", 75, "", "Puppet Zoner"),
    "4": BurnableDan("Burnable Dan", 75, "", "Zoner"),
    "5": HughMann("Hugh-Mann", 75, "", "Big Wrench Installer"),
    "6": JohnCameraman("John Cameraman", 75, "", "Scaling Joke Character"),
    "7": PerryPenguin("Perry Penguin", 75, "", "Rushdown"),
    "8": Catscade("Catscade", 75, "", "Evil Incineroar"),
    "9": BigKeyBoy("Big Key Boy", 75, "", "Boy Wonder"),
    "10": Incrediboy("Incrediboy", 75, "", "Joke Character")
}


def pick(name):
    print(f"\n{name}, choose character:")
    for k, v in roster.items():
        print(f"{k}. {v.name} - {v.description}")
    return roster[input("Pick: ")]


def play():
    p1 = pick("Player 1")
    p2 = pick("Player 2")

    game = Game(p1, p2)

    while not game.is_over():
        print("\n" + "="*30)
        game.status()
        game.take_turn()

    print(f"\n🏆 {game.winner()} wins!")


if __name__ == "__main__":
    play()
