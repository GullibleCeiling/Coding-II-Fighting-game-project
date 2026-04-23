import curses
from curses import wrapper
import random

class Character:
    """Base class for all characters"""
    def __init__(self, name, hp, attack, defense, icon):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.icon = icon
        self.x = 0
        self.y = 0
    
    def take_damage(self, damage):
        """Reduce HP by damage amount"""
        self.hp = max(0, self.hp - damage)
    
    def heal(self, amount):
        """Increase HP up to max"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def is_alive(self):
        """Check if character is still alive"""
        return self.hp > 0
    
    def calculate_damage(self, defender):
        """Calculate damage with randomness"""
        base_damage = self.attack - (defender.defense // 2)
        variance = random.randint(-3, 8)
        final_damage = max(1, base_damage + variance)
        return final_damage


class Warrior(Character):
    """Strong defender"""
    def __init__(self, name="Warrior"):
        super().__init__(name, hp=120, attack=18, defense=8, icon="W")


class Archer(Character):
    """High attack damage"""
    def __init__(self, name="Archer"):
        super().__init__(name, hp=80, attack=22, defense=4, icon="A")


class Mage(Character):
    """Balanced stats"""
    def __init__(self, name="Mage"):
        super().__init__(name, hp=70, attack=16, defense=3, icon="M")


game_data = {
    'player1': None,
    'player2': None,
    'map_width': 20,
    'map_height': 10,
    'in_combat': False,
    'combat_log': [],
    'game_over': False
}


def draw_map(stdscr):
    """Draw the game map with both players"""
    stdscr.clear()
    
    player1 = game_data['player1']
    player2 = game_data['player2']
    
    # Draw border and map
    for y in range(game_data['map_height']):
        for x in range(game_data['map_width']):
            if player1.x == x and player1.y == y:
                stdscr.addstr(y, x, player1.icon, curses.color_pair(2))
            elif player2.x == x and player2.y == y:
                stdscr.addstr(y, x, player2.icon, curses.color_pair(3))
            else:
                stdscr.addstr(y, x, '.', curses.color_pair(1))
    
    # Draw stats below map
    stats_y = game_data['map_height'] + 1
    stdscr.addstr(stats_y, 0, f"{player1.name} (P1): HP {player1.hp}/{player1.max_hp}", curses.color_pair(2))
    stdscr.addstr(stats_y + 1, 0, f"{player2.name} (P2): HP {player2.hp}/{player2.max_hp}", curses.color_pair(3))
    
    # Instructions
    stdscr.addstr(stats_y + 3, 0, "P1 Controls: WASD to move, space to attack")
    stdscr.addstr(stats_y + 4, 0, "P2 Controls: Arrow keys to move, Enter to attack")
    
    stdscr.refresh()


def check_collision():
    """Check if players are adjacent and can fight"""
    p1 = game_data['player1']
    p2 = game_data['player2']
    
    # Check if next to each other (distance = 1)
    distance = abs(p1.x - p2.x) + abs(p1.y - p2.y)
    return distance == 1


def handle_combat(attacker, defender, action):
    """Handle a single combat action"""
    if action == 'attack':
        damage = attacker.calculate_damage(defender)
        defender.take_damage(damage)
        game_data['combat_log'].append(f"{attacker.name} attacked! Dealt {damage} damage.")
    elif action == 'defend':
        game_data['combat_log'].append(f"{attacker.name} defended!")


def draw_combat_screen(stdscr):
    """Draw the combat screen"""
    stdscr.clear()
    
    p1 = game_data['player1']
    p2 = game_data['player2']
    
    # Title
    stdscr.addstr(0, 5, "=== COMBAT ===", curses.color_pair(1) | curses.A_BOLD)
    
    # Player 1 vs Player 2
    stdscr.addstr(2, 2, f"{p1.name}: {p1.hp}/{p1.max_hp} HP", curses.color_pair(2))
    stdscr.addstr(3, 2, f"{p2.name}: {p2.hp}/{p2.max_hp} HP", curses.color_pair(3))
    
    # Combat log
    stdscr.addstr(5, 2, "Combat Log:", curses.color_pair(1))
    for i, msg in enumerate(game_data['combat_log'][-5:]):
        stdscr.addstr(6 + i, 2, msg[:40], curses.color_pair(1))
    
    # Instructions
    stdscr.addstr(12, 2, "P1: Space to attack, D to defend")
    stdscr.addstr(13, 2, "P2: Enter to attack, D to defend")
    
    stdscr.refresh()


def move_player(player, key):
    """Move a player on the map"""
    # Player 1: WASD
    if player == game_data['player1']:
        if key == ord('w') and player.y > 0:
            player.y -= 1
        elif key == ord('s') and player.y < game_data['map_height'] - 1:
            player.y += 1
        elif key == ord('a') and player.x > 0:
            player.x -= 1
        elif key == ord('d') and player.x < game_data['map_width'] - 1:
            player.x += 1
    
    # Player 2: Arrow keys
    elif player == game_data['player2']:
        if key == curses.KEY_UP and player.y > 0:
            player.y -= 1
        elif key == curses.KEY_DOWN and player.y < game_data['map_height'] - 1:
            player.y += 1
        elif key == curses.KEY_LEFT and player.x > 0:
            player.x -= 1
        elif key == curses.KEY_RIGHT and player.x < game_data['map_width'] - 1:
            player.x += 1


def main(stdscr):
    # Setup colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_CYAN, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)
    
    stdscr.nodelay(True)
    stdscr.timeout(50)
    
    # Create players
    game_data['player1'] = Warrior(name="Player 1")
    game_data['player2'] = Archer(name="Player 2")
    
    # Starting positions
    game_data['player1'].x = 2
    game_data['player1'].y = 2
    game_data['player2'].x = 17
    game_data['player2'].y = 7
    
    game_data['in_combat'] = False
    
    while not game_data['game_over']:
        # Check if both players are alive
        if not game_data['player1'].is_alive():
            draw_combat_screen(stdscr)
            stdscr.addstr(15, 2, f"{game_data['player2'].name} WINS! Press Q to quit")
            if stdscr.getch() == ord('q'):
                game_data['game_over'] = True
            continue
        elif not game_data['player2'].is_alive():
            draw_combat_screen(stdscr)
            stdscr.addstr(15, 2, f"{game_data['player1'].name} WINS! Press Q to quit")
            if stdscr.getch() == ord('q'):
                game_data['game_over'] = True
            continue
        
        if game_data['in_combat']:
            draw_combat_screen(stdscr)
            
            # Check if still adjacent
            if not check_collision():
                game_data['in_combat'] = False
                game_data['combat_log'] = []
                continue
            
            # Handle combat input
            key = stdscr.getch()
            
            if key == ord(' '):  # Player 1 attack
                handle_combat(game_data['player1'], game_data['player2'], 'attack')
                handle_combat(game_data['player2'], game_data['player1'], 'attack')
            elif key == ord('d'):  # Player 1 defend
                game_data['combat_log'].append(f"{game_data['player1'].name} defended!")
                handle_combat(game_data['player2'], game_data['player1'], 'attack')
        else:
            draw_map(stdscr)
            
            # Handle movement
            key = stdscr.getch()
            
            if key == ord('q'):
                game_data['game_over'] = True
            elif key == ord('w') or key == ord('s') or key == ord('a') or key == ord('d'):
                move_player(game_data['player1'], key)
            elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                move_player(game_data['player2'], key)
            
            # Check for collision (combat start)
            if check_collision():
                game_data['in_combat'] = True
                game_data['combat_log'] = [f"{game_data['player1'].name} encounters {game_data['player2'].name}!"]


wrapper(main)