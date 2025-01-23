# FILE: game.py
import unicurses
import random
import time
import json
import uuid
from player import Player
from asteroid import Asteroid

WORLD_WIDTH = 100
WORLD_HEIGHT = 100
NUM_PLANETS = 10

def load_players():
    try:
        with open('players.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_players(players):
    with open('players.json', 'w') as file:
        json.dump(players, file, indent=4)

def get_string_input(stdscr, prompt, y, x):
    unicurses.echo()
    unicurses.curs_set(1)
    
    unicurses.move(y, x)
    unicurses.addstr(prompt)
    
    input_str = ""
    while True:
        ch = unicurses.getch()
        if ch in [10, 13]:  # Enter key
            break
        elif ch == 27:  # Escape key
            input_str = None
            break
        elif ch == 8 or ch == 127:  # Backspace
            if input_str:
                input_str = input_str[:-1]
                unicurses.move(y, x + len(prompt))
                unicurses.addstr(" " * len(input_str) + " ")
                unicurses.move(y, x + len(prompt))
                unicurses.addstr(input_str)
        else:
            input_str += chr(ch)
    
    unicurses.noecho()
    unicurses.curs_set(0)
    return input_str

def create_player_menu(stdscr):
    sh, sw = unicurses.getmaxyx(stdscr)
    
    while True:
        unicurses.clear()
        name = get_string_input(stdscr, "Enter player name: ", sh//2, sw//4)
        
        if name:
            player_id = str(uuid.uuid4())[:8]
            new_player = {
                "playerId": player_id,
                "name": name,
                "inventory": {
                    "fuel": 100,
                    "iron": 0,
                    "gold": 0
                },
                "currentPlanetId": None
            }
            
            players = load_players()
            players.append(new_player)
            save_players(players)
            
            unicurses.clear()
            unicurses.move(sh//2, sw//4)
            unicurses.addstr(f"Player {name} created successfully!")
            unicurses.refresh()
            unicurses.napms(2000)
            return player_id, name
        else:
            return None, None

def select_player_menu(stdscr):
    players = load_players()
    if not players:
        sh, sw = unicurses.getmaxyx(stdscr)
        unicurses.clear()
        unicurses.move(sh//2, sw//4)
        unicurses.addstr("No players found. Please create a player first.")
        unicurses.refresh()
        unicurses.napms(2000)
        return None, None

    current_row = 0
    while True:
        sh, sw = unicurses.getmaxyx(stdscr)
        unicurses.clear()
        
        unicurses.move(sh//4, sw//4)
        unicurses.addstr("Select Player:")
        
        for idx, player in enumerate(players):
            unicurses.move(sh//4 + idx + 2, sw//4)
            if idx == current_row:
                unicurses.attron(unicurses.A_REVERSE)
            unicurses.addstr(f"{player['name']} (Fuel: {player['inventory']['fuel']})")
            if idx == current_row:
                unicurses.attroff(unicurses.A_REVERSE)
        
        unicurses.refresh()
        
        key = unicurses.getch()
        if key == unicurses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == unicurses.KEY_DOWN and current_row < len(players) - 1:
            current_row += 1
        elif key in [unicurses.KEY_ENTER, 10, 13]:
            return players[current_row]["playerId"], players[current_row]["name"]
        elif key == 27:  # Escape
            return None, None

def draw_menu(stdscr):
    sh, sw = unicurses.getmaxyx(stdscr)
    menu = ["Start Game", "Create Player", "Select Player", "Exit"]
    current_row = 0

    while True:
        unicurses.clear()
        for idx, row in enumerate(menu):
            x = sw // 2 - len(row) // 2
            y = sh // 2 - len(menu) // 2 + idx
            unicurses.move(y, x)
            if idx == current_row:
                unicurses.attron(unicurses.A_REVERSE)
                unicurses.addstr(row)
                unicurses.attroff(unicurses.A_REVERSE)
            else:
                unicurses.addstr(row)
        unicurses.refresh()

        key = unicurses.getch()
        if key == unicurses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == unicurses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key in [unicurses.KEY_ENTER, 10, 13]:
            return menu[current_row].lower().replace(" ", "_")

def generate_planets():
    planets = []
    for _ in range(NUM_PLANETS):
        x = random.randint(0, WORLD_WIDTH - 1)
        y = random.randint(0, WORLD_HEIGHT - 1)
        size = random.randint(1, 3)  # Random size between 1 and 3
        planets.append((x, y, size))
    return planets

def generate_asteroids(num_asteroids, sw):
    return [Asteroid(random.randint(0, sw - 1), 0) for _ in range(num_asteroids)]

def draw_world(buffer, player, planets, asteroids):
    sh, sw = unicurses.getmaxyx(buffer)
    top = max(0, player.position["y"] - sh // 2)
    left = max(0, player.position["x"] - sw // 2)

    # Clear the buffer
    unicurses.werase(buffer)

    # Draw planets
    for planet_x, planet_y, size in planets:
        if top <= planet_y < top + sh and left <= planet_x < left + sw:
            for i in range(size):
                for j in range(size):
                    if top <= planet_y + i < top + sh and left <= planet_x + j < left + sw:
                        unicurses.mvwaddch(buffer, planet_y + i - top, planet_x + j - left, ord('O'))

    # Draw asteroids
    for asteroid in asteroids:
        if asteroid.visible and top <= asteroid.y < top + sh and left <= asteroid.x < left + sw:
            unicurses.mvwaddch(buffer, asteroid.y - top, asteroid.x - left, ord('X'))

    # Draw player
    unicurses.mvwaddch(buffer, player.position["y"] - top, player.position["x"] - left, ord('@'))

    # Refresh the buffer
    unicurses.wnoutrefresh(buffer)
    unicurses.doupdate()

def is_collision_with_planet(x, y, planets):
    for planet_x, planet_y, size in planets:
        if (planet_x <= x < planet_x + size and 
            planet_y <= y < planet_y + size):
            return True
    return False

def gameover():
    unicurses.addstr("Game Over!")

def main(stdscr):
    unicurses.curs_set(0)
    sh, sw = unicurses.getmaxyx(stdscr)
    unicurses.keypad(stdscr, True)

    current_player_id = None
    current_player_name = None

    while True:
        choice = draw_menu(stdscr)
        if choice == "start_game":
            if current_player_id:
                break
            else:
                unicurses.clear()
                unicurses.move(sh//2, sw//4)
                unicurses.addstr("Please select a player first!")
                unicurses.refresh()
                unicurses.napms(2000)
        elif choice == "create_player":
            current_player_id, current_player_name = create_player_menu(stdscr)
        elif choice == "select_player":
            selected_id, selected_name = select_player_menu(stdscr)
            if selected_id:
                current_player_id = selected_id
                current_player_name = selected_name
        elif choice == "exit":
            return

    # Set up non-blocking input with zero delay
    unicurses.nodelay(stdscr, True)

    # Create buffer window for double buffering
    buffer = unicurses.newwin(sh, sw, 0, 0)
    unicurses.keypad(buffer, True)

    # Create player instance
    player = Player(current_player_name)
    player.position["x"] = WORLD_WIDTH // 2
    player.position["y"] = WORLD_HEIGHT // 2

    # Game settings
    ASTEROID_SPEED = 15.0  # positions per second
    ASTEROID_FREQUENCY = 0.1  # new asteroids per second
    last_move_time = time.time()
    last_asteroid_time = time.time()
    accumulated_movement = 0.0

    # Generate random planets
    planets = generate_planets()

    # Generate random asteroids
    asteroids = generate_asteroids(5, sw)

    while True:
        key = unicurses.getch()

        # Store old position for collision check
        old_x = player.position["x"]
        old_y = player.position["y"]

        # Handle player movement
        if key == unicurses.KEY_UP:
            player.move_up()
            player.position["y"] = max(0, player.position["y"])
        elif key == unicurses.KEY_DOWN:
            player.move_down()
            player.position["y"] = min(WORLD_HEIGHT - 1, player.position["y"])
        elif key == unicurses.KEY_LEFT:
            player.move_left()
            player.position["x"] = max(0, player.position["x"])
        elif key == unicurses.KEY_RIGHT:
            player.move_right()
            player.position["x"] = min(WORLD_WIDTH - 1, player.position["x"])
        elif key == ord('q'):
            break

        # Check for collision with planets and revert if needed
        if is_collision_with_planet(player.position["x"], player.position["y"], planets):
            player.position["x"] = old_x
            player.position["y"] = old_y

        # Calculate time-based movement
        current_time = time.time()
        elapsed = current_time - last_move_time
        last_move_time = current_time

        accumulated_movement += elapsed * ASTEROID_SPEED
        moves = int(accumulated_movement)
        accumulated_movement -= moves

        # Move asteroids down based on accumulated movement
        new_asteroids = []
        for asteroid in asteroids:
            asteroid.move_down(moves)
            if asteroid.y < WORLD_HEIGHT - 1:
                new_asteroids.append(asteroid)
            else:
                new_asteroids.append(Asteroid(random.randint(0, WORLD_WIDTH - 1), 0))
        asteroids = new_asteroids

        # Generate new asteroids based on frequency
        if current_time - last_asteroid_time >= ASTEROID_FREQUENCY:
            last_asteroid_time = current_time
            asteroids.append(Asteroid(random.randint(0, WORLD_WIDTH - 1), 0))

        # Remove asteroids that collide with planets
        asteroids = [ast for ast in asteroids if not is_collision_with_planet(ast.x, ast.y, planets)]

        # Check for collision with player
        # Check for collision with player
        for asteroid in asteroids:
            if asteroid.visible and asteroid.x == player.position["x"] and asteroid.y == player.position["y"]:
                player.health -= 25
                asteroid.visible = False
                if player.health <= 0:
                    unicurses.clear()
                    unicurses.move(sh // 2, sw // 2 - len("Game Over!") // 2)
                    gameover()
                    unicurses.refresh()
                    unicurses.napms(2000)
                    return

        # Remove invisible asteroids
        asteroids = [ast for ast in asteroids if ast.visible]

        draw_world(buffer, player, planets, asteroids)
        unicurses.move(0, 0)
        unicurses.addstr(f"Life: {player.health}")

if __name__ == "__main__":
    unicurses.wrapper(main)