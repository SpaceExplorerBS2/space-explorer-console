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

    # Clear the buffer and reset attributes
    unicurses.werase(buffer)
    unicurses.wattrset(buffer, unicurses.color_pair(3))  # Reset to default white

    # Set color based on health percentage
    health_color = unicurses.color_pair(3)  # default white
    if player.health < 30:
        health_color = unicurses.color_pair(1)  # red
    elif player.health < 50:
        health_color = unicurses.color_pair(2)  # yellow
        
    # Set color based on fuel percentage
    fuel_color = unicurses.color_pair(3)  # default white
    if player.fuel < 30:
        fuel_color = unicurses.color_pair(1)  # red
    elif player.fuel < 50:
        fuel_color = unicurses.color_pair(2)  # yellow

    # Draw health with color
    unicurses.wattrset(buffer, health_color)
    unicurses.mvwaddstr(buffer, 0, 0, f"Life: {player.health}")
    
    # Draw fuel with color
    unicurses.wattrset(buffer, fuel_color)
    unicurses.mvwaddstr(buffer, 1, 0, f"Fuel: {player.fuel}")

    # Reset color to default for remaining drawing
    unicurses.wattrset(buffer, unicurses.color_pair(3))

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

def game_loop(buffer, player, planets, sh, sw):
    # Game settings
    ASTEROID_SPEED = 15.0  # positions per second
    ASTEROID_FREQUENCY = 50  # new asteroids per second
    FUEL_REGEN_TIME = 15.0  # seconds to wait before regenerating fuel
    FUEL_REGEN_AMOUNT = 15  # amount of fuel to regenerate
    REFRESH_RATE = 0.05  # seconds between screen refreshes
    
    last_move_time = time.time()
    last_asteroid_time = time.time()
    last_movement_time = time.time()  # Track when player last moved
    last_refresh_time = time.time()   # Track when screen was last refreshed
    accumulated_movement = 0.0

    # Set input to non-blocking
    unicurses.nodelay(buffer, True)

    # Generate random planets
    asteroids = []
    asteroids = generate_asteroids(5, sw)

    while True:
        current_time = time.time()
        
        # Get user input (non-blocking)
        key = unicurses.wgetch(buffer)
        
        # Store old position for collision check
        old_x = player.position["x"]
        old_y = player.position["y"]
        moved = False

        # Handle player movement if there was input
        if key != -1:  # -1 means no key was pressed
            if key == unicurses.KEY_UP:
                if player.fuel > 0:
                    player.move_up()
                    player.position["y"] = max(0, player.position["y"])
                    moved = True
            elif key == unicurses.KEY_DOWN:
                if player.fuel > 0:
                    player.move_down()
                    player.position["y"] = min(WORLD_HEIGHT - 1, player.position["y"])
                    moved = True
            elif key == unicurses.KEY_LEFT:
                if player.fuel > 0:
                    player.move_left()
                    player.position["x"] = max(0, player.position["x"])
                    moved = True
            elif key == unicurses.KEY_RIGHT:
                if player.fuel > 0:
                    player.move_right()
                    player.position["x"] = min(WORLD_WIDTH - 1, player.position["x"])
                    moved = True
            elif key == ord('q'):
                break

            # Check for collision with planets and revert if needed
            if is_collision_with_planet(player.position["x"], player.position["y"], planets):
                player.position["x"] = old_x
                player.position["y"] = old_y
                moved = False

        # Update last movement time if player moved
        if moved:
            last_movement_time = current_time
        else:
            # Check if player has been still long enough to regenerate fuel
            if current_time - last_movement_time >= FUEL_REGEN_TIME and player.fuel < 100:
                player.add_fuel(FUEL_REGEN_AMOUNT)
                last_movement_time = current_time  # Reset timer after regenerating

        # Game over if out of fuel
        if player.fuel <= 0:
            unicurses.clear()
            unicurses.move(sh // 2, sw // 2 - len("Out of Fuel! Game Over!") // 2)
            unicurses.addstr("Out of Fuel! Game Over!")
            unicurses.refresh()
            unicurses.napms(2000)
            return

        # Calculate time-based movement for asteroids
        elapsed = current_time - last_move_time
        accumulated_movement += ASTEROID_SPEED * elapsed
        
        while accumulated_movement >= 1.0:
            # Move all asteroids down
            for asteroid in asteroids:
                asteroid.y += 1
                if asteroid.y >= WORLD_HEIGHT:
                    asteroid.visible = False
            accumulated_movement -= 1.0

        last_move_time = current_time

        # Generate new asteroids
        if current_time - last_asteroid_time > 1.0 / ASTEROID_FREQUENCY:
            new_asteroid_x = random.randint(0, WORLD_WIDTH - 1)
            asteroids.append(Asteroid(new_asteroid_x, 0))
            last_asteroid_time = current_time

        # Check for collisions with asteroids
        for asteroid in asteroids:
            if asteroid.visible and asteroid.x == player.position["x"] and asteroid.y == player.position["y"]:
                player.health -= 25
                asteroid.visible = False

                if player.health <= 0:
                    unicurses.clear()
                    unicurses.move(sh // 2, sw // 2 - len("Game Over!") // 2)
                    unicurses.addstr("Game Over!")
                    unicurses.refresh()
                    unicurses.napms(2000)
                    return

        # Remove invisible asteroids
        asteroids = [ast for ast in asteroids if ast.visible]

        # Update screen at regular intervals
        if current_time - last_refresh_time >= REFRESH_RATE:
            draw_world(buffer, player, planets, asteroids)
            last_refresh_time = current_time

        # Small sleep to prevent CPU overuse
        time.sleep(0.01)

def main(stdscr):
    unicurses.curs_set(0)
    unicurses.start_color()
    unicurses.init_pair(1, unicurses.COLOR_RED, unicurses.COLOR_BLACK)    # For critical levels (<30%)
    unicurses.init_pair(2, unicurses.COLOR_YELLOW, unicurses.COLOR_BLACK) # For warning levels (<50%)
    unicurses.init_pair(3, unicurses.COLOR_WHITE, unicurses.COLOR_BLACK)  # For normal levels
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

    # Generate random planets
    planets = generate_planets()

    game_loop(buffer, player, planets, sh, sw)

if __name__ == "__main__":
    unicurses.wrapper(main)