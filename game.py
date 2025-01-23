# FILE: game.py
import unicurses
import random
import time
import json
import uuid
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
            return player_id
        else:
            return None

def select_player_menu(stdscr):
    players = load_players()
    if not players:
        sh, sw = unicurses.getmaxyx(stdscr)
        unicurses.clear()
        unicurses.move(sh//2, sw//4)
        unicurses.addstr("No players found. Please create a player first.")
        unicurses.refresh()
        unicurses.napms(2000)
        return None

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
            return players[current_row]["playerId"]
        elif key == 27:  # Escape
            return None

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
    return [(random.randint(0, sw - 1), 0) for _ in range(num_asteroids)]

def draw_world(buffer, player_x, player_y, planets, asteroids):
    sh, sw = unicurses.getmaxyx(buffer)
    top = max(0, player_y - sh // 2)
    left = max(0, player_x - sw // 2)

    # Clear the buffer
    unicurses.werase(buffer)

    # Draw planets
    for planet_x, planet_y, size in planets:
        if top <= planet_y < top + sh and left <= planet_x < left + sw:
            for i in range(size):
                for j in range(size):
                    if top <= planet_y + i < top + sh and left <= planet_x + j < left + sw:
                        unicurses.mvwaddch(buffer, planet_y + i - top, planet_x + j - left, 'O')

    # Draw asteroids
    for ax, ay in asteroids:
        if top <= ay < top + sh and left <= ax < left + sw:
            unicurses.mvwaddch(buffer, ay - top, ax - left, 'X')

    # Draw player
    unicurses.mvwaddch(buffer, player_y - top, player_x - left, '@')

    # Refresh the buffer
    unicurses.wnoutrefresh(buffer)
    unicurses.doupdate()

def is_collision_with_planet(player_x, player_y, planets):
    for planet_x, planet_y, size in planets:
        if planet_x <= player_x < planet_x + size and planet_y <= player_y < planet_y + size:
            return True
    return False

def main(stdscr):
    unicurses.curs_set(0)
    sh, sw = unicurses.getmaxyx(stdscr)
    unicurses.keypad(stdscr, True)

    current_player_id = None

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
            current_player_id = create_player_menu(stdscr)
        elif choice == "select_player":
            selected_id = select_player_menu(stdscr)
            if selected_id:
                current_player_id = selected_id
        elif choice == "exit":
            return

    # Set up non-blocking input with zero delay
    unicurses.nodelay(stdscr, True)

    # Create buffer window for double buffering
    buffer = unicurses.newwin(sh, sw, 0, 0)
    unicurses.keypad(buffer, True)

    # Initial position of the player
    player_x, player_y = WORLD_WIDTH // 2, WORLD_HEIGHT // 2

    # Player's life
    player_life = 100

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

        new_x, new_y = player_x, player_y
        if key == unicurses.KEY_UP:
            new_y = max(0, player_y - 1)
        elif key == unicurses.KEY_DOWN:
            new_y = min(WORLD_HEIGHT - 1, player_y + 1)
        elif key == unicurses.KEY_LEFT:
            new_x = max(0, player_x - 1)
        elif key == unicurses.KEY_RIGHT:
            new_x = min(WORLD_WIDTH - 1, player_x + 1)
        elif key == ord('q'):
            break

        # Check for collision with planets
        if not is_collision_with_planet(new_x, new_y, planets):
            player_x, player_y = new_x, new_y

        # Calculate time-based movement
        current_time = time.time()
        elapsed = current_time - last_move_time
        last_move_time = current_time
        
        accumulated_movement += elapsed * ASTEROID_SPEED
        moves = int(accumulated_movement)
        accumulated_movement -= moves

        # Move asteroids down based on accumulated movement
        new_asteroids = []
        for ax, ay in asteroids:
            new_y = ay + moves
            if new_y < WORLD_HEIGHT - 1:
                new_asteroids.append((ax, new_y))
            else:
                new_asteroids.append((random.randint(0, WORLD_WIDTH - 1), 0))
        asteroids = new_asteroids

        # Generate new asteroids based on frequency
        if current_time - last_asteroid_time >= ASTEROID_FREQUENCY:
            last_asteroid_time = current_time
            asteroids.append((random.randint(0, WORLD_WIDTH - 1), 0))

        # Check for collision with planets
        asteroids = [(ax, ay) for ax, ay in asteroids if not is_collision_with_planet(ax, ay, planets)]

        # Check for collision with player
        if (player_x, player_y) in asteroids:
            player_life -= 25
            if player_life <= 0:
                unicurses.clear()
                unicurses.move(sh // 2, sw // 2 - len("Game Over!") // 2)
                unicurses.addstr("Game Over!")
                unicurses.refresh()
                unicurses.napms(2000)
                break

        draw_world(buffer, player_x, player_y, planets, asteroids)
        unicurses.move(0, 0)
        unicurses.addstr(f"Life: {player_life}")

if __name__ == "__main__":
    unicurses.wrapper(main)