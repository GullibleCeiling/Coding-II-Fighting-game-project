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
        elif move == "kick":
            dmg = 4
            other.take_damage(dmg)
            return f"🦵 Kick for {dmg}"
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
        elif move == "kick":
            dmg = 4
            other.take_damage(dmg)
            return f"🦵 Kick for {dmg}"
        elif move == "punch":
            dmg = 5
            other.take_damage(dmg)
            return f"👊 Punch for {dmg}"


class BrickAndMortar(Character):
    def attack(self, other, move):
        if move == "brick":
            self.pending_actions.append({"turns": 2, "damage": 8, "target": other})
            return "🧱 Mortar launches Brick (hits in 2 turns!)"
        elif move == "kick":
            dmg = 4
            other.take_damage(dmg)
            return f"🦵 Kick for {dmg}"


class BurnableDan(Character):
    def attack(self, other, move):
        if move == "fireball":
            dmg = 3
            other.take_damage(dmg)
            return f"🔥 Fireball hits for {dmg}"
        elif move == "kick":
            dmg = 4
            other.take_damage(dmg)
            return f"🦵 Kick for {dmg}"


class HughMann(Character):
    def attack(self, other, move):
        if move == "slashes":
            dmg = 6
            other.take_damage(dmg)
            return f"⚔️ Slashes for {dmg}"
        elif move == "bonk":
            self.pending_actions.append({"turns": 2, "hits": 3, "target": other})
            return "🔨 Judgement Bonk incoming (3 hits, slow!)"


class JohnCameraman(Character):
    def attack(self, other, move):
        if move == "camera":
            self.meter += 1
            dmg = self.meter
            other.take_damage(dmg)
            return f"📸 Camera hits for {dmg} (meter: {self.meter})"


class PerryPenguin(Character):
    def attack(self, other, move):
        if move == "rush":
            dmg = random.randint(4, 9)
            other.take_damage(dmg)
            return f"🐧 Perry rushes for {dmg}"
        elif move == "kick":
            dmg = 4
            other.take_damage(dmg)
            return f"🦵 Kick for {dmg}"


class Catscade(Character):
    def attack(self, other, move):
        if move == "avenge":
            self.next_bonus = 0
            return "😾 Catscade prepares Avenge!"
        elif move == "hit":
            dmg = 6 + getattr(self, "next_bonus", 0)
            self.next_bonus = 0
            other.take_damage(dmg)
            return f"🐱 Hit for {dmg}"


class BigKeyBoy(Character):
    def attack(self, other, move):
        if move == "crown":
            self.pending_actions.append({"turns": 2, "damage": 8, "hits": 2, "target": other})
            return "👑 Crown Toss (delayed double hit!)"


class Incrediboy(Character):
    def attack(self, other, move):
        dmg = 4
        other.take_damage(dmg)
        return f"💥 Incrediboy hits for {dmg}"


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
        print("1 Punch | 2 Kick | 3 Special")

        move = input("Move: ")

        if isinstance(p, Feignaz):
            action = "grapple" if move == "3" else "kick" if move == "2" else "punch"
        elif isinstance(p, Kazuki):
            action = "rush" if move == "3" else "kick" if move == "2" else "punch"
        elif isinstance(p, BrickAndMortar):
            action = "brick" if move == "3" else "kick"
        elif isinstance(p, BurnableDan):
            action = "fireball" if move == "3" else "kick"
        elif isinstance(p, HughMann):
            action = "bonk" if move == "3" else "slashes"
        elif isinstance(p, JohnCameraman):
            action = "camera"
        elif isinstance(p, PerryPenguin):
            action = "rush" if move == "3" else "kick"
        elif isinstance(p, Catscade):
            action = "avenge" if move == "3" else "hit"
        elif isinstance(p, BigKeyBoy):
            action = "crown" if move == "3" else "punch"
        else:
            action = "punch"

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
    "1": Feignaz("Feignaz", 30, "", "Grappler"),
    "2": Kazuki("Kazuki", 28, "", "Rushdown"),
    "3": BrickAndMortar("Brick & Mortar", 32, "", "Puppet Zoner"),
    "4": BurnableDan("Burnable Dan", 26, "", "Zoner"),
    "5": HughMann("Hugh-Mann", 35, "", "Big Wrench Installer"),
    "6": JohnCameraman("John Cameraman", 20, "", "Scaling Joke Character"),
    "7": PerryPenguin("Perry Penguin", 28, "", "Rushdown"),
    "8": Catscade("Catscade", 30, "", "Evil Incineroar"),
    "9": BigKeyBoy("Big Key Boy", 30, "", "Boy Wonder"),
    "10": Incrediboy("Incrediboy", 25, "", "Joke Character")
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
