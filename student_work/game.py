import random
import time


# =========================
# ASCII ART
# =========================

FEIGNAZ_ART = r"""🤼 FEIGNAZ"""
KAZUKI_ART = r"""⚡ KAZUKI"""
BRICK_MORTAR_ART = r"""🧱 BRICK & MORTAR"""
BURNABLE_DAN_ART = r"""🔥 BURNABLE DAN"""
HUGH_MANN_ART = r"""🔧 HUGH-MANN"""
JOHN_CAMERAMAN_ART = r"""📹 JOHN CAMERAMAN"""
PERRY_PENGUIN_ART = r"""🐧 PERRY PENGUIN"""
CATASCADE_ART = r"""😾 CATASCADE"""
BIG_KEY_BOY_ART = r"""👑 BIG KEY BOY"""
INCREDIBOY_ART = r"""💥 INCREDIBOY"""


# =========================
# TAUNTS
# =========================

TAUNT_QUOTES = {
    "Feignaz": "🤼 'Come here, I just want to talk.'",
    "Kazuki": "⚡ 'Too slow!'",
    "Brick & Mortar": "🧱 'We built different.'",
    "Burnable Dan": "🔥 'This is fine.'",
    "Hugh-Mann": "🔧 'Judgement is inevitable.'",
    "John Cameraman": "📸 'Smile, you're on camera!'",
    "Perry Penguin": "🐧 'Wark wark!'",
    "Catscade": "😾 'You will regret that.'",
    "Big Key Boy": "👑 'The crown always wins.'",
    "Incrediboy": "💥 'I'm incredible!'"
}


# =========================
# BASE CHARACTER
# =========================

class Character:
    def __init__(self, name, health, art, description):
        self.name = name
        self.max_health = health
        self.health = health
        self.art = art
        self.description = description

        self.pending_actions = []
        self.meter = 0  # 0–5 max

    def is_alive(self):
        return self.health > 0

    def take_damage(self, dmg):
        self.health = max(0, self.health - dmg)

    def hp_bar(self):
        ratio = self.health / self.max_health
        bar = "█" * int(ratio * 20) + "░" * (20 - int(ratio * 20))
        return f"[{bar}] {self.health}/{self.max_health}"

    # ✅ meter capped at 5
    def taunt(self):
        if self.meter < 5:
            self.meter += 1
        return f"{TAUNT_QUOTES.get(self.name, self.name + ' taunts!')} (meter: {self.meter}/5)"


# =========================
# CHARACTERS
# =========================

class Feignaz(Character):
    def attack(self, other, move):
        if move == "grapple":
            other.take_damage(7)
            return "🤼 Grapple 7"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                other.take_damage(20)
                return "🤼 SPECIAL GRAPPLE (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()

        else:
            other.take_damage(5)
            return "👊 Punch 5"


class Kazuki(Character):
    def attack(self, other, move):
        if move == "rush":
            dmg = random.randint(2, 10)
            other.take_damage(dmg)
            return f"⚡ Rush {dmg}"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                dmg = random.randint(10, 20)
                other.take_damage(dmg)
                return f"⚡ OVERDRIVE {dmg} (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()

        else:
            other.take_damage(5)
            return "👊 Punch 5"


class BrickAndMortar(Character):
    def attack(self, other, move):
        if move == "brick":
            self.pending_actions.append({"turns": 2, "damage": 8, "target": other})
            return "🧱 Brick incoming"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                self.pending_actions.append({"turns": 1, "damage": 15, "hits": 2, "target": other})
                return "🧱 BUILDING COLLAPSE (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()


class BurnableDan(Character):
    def attack(self, other, move):
        if move == "fireball":
            other.take_damage(3)
            return "🔥 Fireball"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                other.take_damage(18)
                return "🔥 INFERNO (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()


class HughMann(Character):
    def attack(self, other, move):
        if move == "bonk":
            self.pending_actions.append({"turns": 2, "hits": 3, "damage": 6, "target": other})
            return "🔨 Bonk incoming"

        elif move == "slashes":
            other.take_damage(6)
            return "⚔️ Slashes"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                other.take_damage(25)
                return "🔧 FINAL JUDGEMENT (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()


class JohnCameraman(Character):
    def attack(self, other, move):
        if move == "camera":
            self.meter += 1
            self.meter = min(5, self.meter)
            dmg = self.meter
            other.take_damage(dmg)
            return f"📸 Camera {dmg}"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                other.take_damage(15)
                return "📸 VIRAL SHOT (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()


class PerryPenguin(Character):
    def attack(self, other, move):
        if move == "rush":
            self.pending_actions.append({"turns": 2, "damage": 8, "hits": 2, "target": other})
            return "🐧 Rush delayed"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                self.pending_actions.append({"turns": 1, "damage": 10, "hits": 4, "target": other})
                return "🐧 ANTARCTIC FURY (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()


class Catscade(Character):
    def attack(self, other, move):
        if move == "avenge":
            self.next_bonus = self.max_health - self.health
            return "😾 Avenge ready"

        elif move == "hit":
            dmg = 6 + getattr(self, "next_bonus", 0)
            self.next_bonus = 0
            other.take_damage(dmg)
            return f"🐱 Hit {dmg}"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                other.take_damage(10 + self.max_health)
                return "😾 REVENGE STRIKE (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()


class BigKeyBoy(Character):
    def attack(self, other, move):
        if move == "crown":
            dmg = random.randint(4, 9)
            other.take_damage(dmg)
            return f"👑 Crown {dmg}"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                dmg = random.randint(15, 25)
                other.take_damage(dmg)
                return "👑 KING'S EXECUTION (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()


class Incrediboy(Character):
    def attack(self, other, move):
        if move == "punch":
            other.take_damage(4)
            return "💥 Punch"

        elif move == "special":
            if self.meter >= 1:
                self.meter -= 1
                other.take_damage(30)
                return "💥 I'M INCREDIBLE (-1 meter)"
            return "Not enough meter!"

        elif move == "taunt":
            return self.taunt()


# =========================
# ROSTER
# =========================

roster = {
    "1": Feignaz("Feignaz", 75, FEIGNAZ_ART, "Grappler"),
    "2": Kazuki("Kazuki", 75, KAZUKI_ART, "Rushdown"),
    "3": BrickAndMortar("Brick & Mortar", 75, BRICK_MORTAR_ART, "Zoner"),
    "4": BurnableDan("Burnable Dan", 75, BURNABLE_DAN_ART, "Zoner"),
    "5": HughMann("Hugh-Mann", 75, HUGH_MANN_ART, "Bruiser"),
    "6": JohnCameraman("John Cameraman", 75, JOHN_CAMERAMAN_ART, "Scaling"),
    "7": PerryPenguin("Perry Penguin", 75, PERRY_PENGUIN_ART, "Rushdown"),
    "8": Catscade("Catscade", 75, CATASCADE_ART, "Risk"),
    "9": BigKeyBoy("Big Key Boy", 75, BIG_KEY_BOY_ART, "All-rounder"),
    "10": Incrediboy("Incrediboy", 75, INCREDIBOY_ART, "Joke")
}


# =========================
# PICK
# =========================

def pick(name):
    print(f"\n{name}, choose character:")
    for k, v in roster.items():
        print(f"{k}. {v.name} - {v.description}")

    choice = input("Pick: ")
    while choice not in roster:
        choice = input("Pick valid number: ")

    template = roster[choice]
    print(template.art)

    return type(template)(
        template.name,
        template.max_health,
        template.art,
        template.description
    )


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

    def resolve(self, player):
        new = []
        for a in player.pending_actions:
            a["turns"] -= 1
            if a["turns"] <= 0:
                if "hits" in a:
                    for _ in range(a["hits"]):
                        a["target"].take_damage(a["damage"])
                else:
                    a["target"].take_damage(a["damage"])
            else:
                new.append(a)
        player.pending_actions = new

    def status(self):
        for p in self.players:
            print(f"{p.name}: {p.hp_bar()} | Meter: {p.meter}/5")

    def is_over(self):
        return any(not p.is_alive() for p in self.players)

    def winner(self):
        alive = [p for p in self.players if p.is_alive()]
        return alive[0].name if alive else "None"

    def take_turn(self):
        p = self.current()
        o = self.other()

        self.resolve(p)

        print(f"\n{p.name}'s turn")
        move = input("1 Punch | 2 Taunt | 3 Special: ")

        if isinstance(p, Feignaz):
            action = "special" if move == "3" else "taunt" if move == "2" else "punch"
        elif isinstance(p, Kazuki):
            action = "special" if move == "3" else "taunt" if move == "2" else "punch"
        elif isinstance(p, BrickAndMortar):
            action = "special" if move == "3" else "brick"
        elif isinstance(p, BurnableDan):
            action = "special" if move == "3" else "fireball"
        elif isinstance(p, HughMann):
            action = "special" if move == "3" else "slashes"
        elif isinstance(p, JohnCameraman):
            action = "special" if move == "3" else "camera"
        elif isinstance(p, PerryPenguin):
            action = "special" if move == "3" else "rush"
        elif isinstance(p, Catscade):
            action = "special" if move == "3" else "hit"
        elif isinstance(p, BigKeyBoy):
            action = "special" if move == "3" else "crown"
        else:
            action = "special" if move == "3" else "punch"

        print(p.attack(o, action))
        self.turn += 1


# =========================
# GAME START
# =========================

def play():
    p1 = pick("Player 1")
    p2 = pick("Player 2")

    game = Game(p1, p2)

    while not game.is_over():
        print("\n" + "=" * 30)
        game.status()
        game.take_turn()

    print("\n" + "█" * 60)
    print(f"🏆 {game.winner().upper()} WINS!")
    print("█" * 60)


if __name__ == "__main__":
    play()
