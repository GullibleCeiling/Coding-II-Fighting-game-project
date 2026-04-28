import pytest
from game import (
    Character,
    Feignaz,
    Kazuki,
    BrickAndMortar,
    BurnableDan,
    HughMann,
    JohnCameraman,
    PerryPenguin,
    Catscade,
    BigKeyBoy,
    Incrediboy,
    Game,
)


# =========================
# BASIC CHARACTER TESTS
# =========================

def test_character_initial_health():
    c = Character("Test", 30, "", "")
    assert c.health == 30


def test_character_is_alive_true():
    c = Character("Test", 10, "", "")
    assert c.is_alive() is True


def test_character_is_alive_false():
    c = Character("Test", 10, "", "")
    c.health = 0
    assert c.is_alive() is False


def test_hp_bar_full():
    c = Character("Test", 20, "", "")
    bar = c.hp_bar()
    assert "20/20" in bar


def test_hp_bar_partial():
    c = Character("Test", 20, "", "")
    c.health = 10
    bar = c.hp_bar()
    assert "10/20" in bar


# =========================
# COMBAT CORE TESTS
# =========================

def test_damage_reduces_health():
    p1 = Character("A", 20, "", "")
    p2 = Character("B", 20, "", "")

    p2.take_damage(5)
    assert p2.health == 15


def test_damage_cannot_go_negative():
    p = Character("A", 5, "", "")
    p.take_damage(999)
    assert p.health == 0


def test_defending_flag():
    p = Character("A", 10, "", "")
    p.defending = True
    assert p.defending is True


# =========================
# HEALING / STATE TESTS
# =========================

def test_healing_does_not_exceed_max():
    c = Character("A", 20, "", "")
    c.health = 18
    c.heal()
    assert c.health <= 20


# =========================
# GAME FLOW TESTS
# =========================

def test_game_current_player():
    p1 = Character("A", 10, "", "")
    p2 = Character("B", 10, "", "")

    g = Game(p1, p2)
    assert g.current() == p1


def test_game_switch_turn():
    p1 = Character("A", 10, "", "")
    p2 = Character("B", 10, "", "")

    g = Game(p1, p2)
    g.turn = 1
    assert g.current() == p2


def test_game_over_when_dead():
    p1 = Character("A", 0, "", "")
    p2 = Character("B", 10, "", "")

    g = Game(p1, p2)
    assert g.is_over() is True


# =========================
# FEIGNAZ TESTS
# =========================

def test_feignaz_grapple():
    p1 = Feignaz("F", 30, "", "")
    p2 = Character("E", 30, "", "")

    msg = p1.attack(p2, "grapple")
    assert "grapples" in msg.lower()


# =========================
# KAZUKI TESTS
# =========================

def test_kazuki_rush():
    p1 = Kazuki("K", 30, "", "")
    p2 = Character("E", 30, "", "")

    msg = p1.attack(p2, "rush")
    assert "rush" in msg.lower()


# =========================
# BRICK & MORTAR TESTS
# =========================

def test_brick_delayed_action():
    p1 = BrickAndMortar("B", 30, "", "")
    p2 = Character("E", 30, "", "")

    msg = p1.attack(p2, "brick")
    assert "brick" in msg.lower()


def test_brick_pending_added():
    p1 = BrickAndMortar("B", 30, "", "")
    p2 = Character("E", 30, "", "")

    p1.attack(p2, "brick")
    assert len(p1.pending_actions) == 1


# =========================
# BURNABLE DAN TESTS
# =========================

def test_fireball_damage_message():
    p1 = BurnableDan("D", 30, "", "")
    p2 = Character("E", 30, "", "")

    msg = p1.attack(p2, "fireball")
    assert "fireball" in msg.lower()


# =========================
# HUGH-MANN TESTS
# =========================

def test_hugh_slashes():
    p1 = HughMann("H", 30, "", "")
    p2 = Character("E", 30, "", "")

    msg = p1.attack(p2, "slashes")
    assert "slashes" in msg.lower()


def test_hugh_bonk_pending():
    p1 = HughMann("H", 30, "", "")
    p2 = Character("E", 30, "", "")

    p1.attack(p2, "bonk")
    assert len(p1.pending_actions) == 1


# =========================
# JOHN CAMERAMAN TESTS
# =========================

def test_john_meter_increases():
    p1 = JohnCameraman("J", 30, "", "")
    p2 = Character("E", 30, "", "")

    p1.attack(p2, "camera")
    assert p1.meter == 1


def test_john_scaling_damage():
    p1 = JohnCameraman("J", 30, "", "")
    p2 = Character("E", 30, "", "")

    p1.meter = 3
    msg = p1.attack(p2, "camera")
    assert "3" in msg


# =========================
# CATSCADE TESTS
# =========================

def test_catscade_avenge_sets_buff():
    p1 = Catscade("C", 30, "", "")
    p2 = Character("E", 30, "", "")

    p1.attack(p2, "avenge")
    assert hasattr(p1, "next_bonus")


def test_catscade_hit_damage():
    p1 = Catscade("C", 30, "", "")
    p2 = Character("E", 30, "", "")

    msg = p1.attack(p2, "hit")
    assert "hit" in msg.lower()


# =========================
# BIG KEY BOY TESTS
# =========================

def test_big_key_pending():
    p1 = BigKeyBoy("B", 30, "", "")
    p2 = Character("E", 30, "", "")

    p1.attack(p2, "crown")
    assert len(p1.pending_actions) == 1


# =========================
# INCREDIBOY TESTS
# =========================

def test_incrediboy_attack():
    p1 = Incrediboy("I", 30, "", "")
    p2 = Character("E", 30, "", "")

    msg = p1.attack(p2, "anything")
    assert "incrediboy" in msg.lower() or "hits" in msg.lower()


# =========================
# GAME INTEGRATION TEST
# =========================

def test_game_has_winner_logic():
    p1 = Character("A", 0, "", "")
    p2 = Character("B", 10, "", "")

    g = Game(p1, p2)
    assert g.winner() == "B"


