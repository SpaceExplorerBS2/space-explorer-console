# FILE: game.py
import unicurses
import random
import time
import json
import uuid
from player import Player
from asteroid import Asteroid
from planet import Planet
from moon import Moon
from sound_manager import SoundManager
from settings_manager import SettingsManager

WORLD_WIDTH = 300
WORLD_HEIGHT = 300
NUM_PLANETS = 10
NUM_MOONS_PER_PLANET = 1
MOON_ORBIT_RADIUS = 5

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
                    "fuel": 500,
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
    sound_manager = SoundManager()
    
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
            sound_manager.play_menu_sound()
        elif key == unicurses.KEY_DOWN and current_row < len(players) - 1:
            current_row += 1
            sound_manager.play_menu_sound()
        elif key in [unicurses.KEY_ENTER, 10, 13]:
            return players[current_row]["playerId"], players[current_row]["name"]
        elif key == 27:  # Escape
            return None, None

def settings_menu(stdscr):
    sh, sw = unicurses.getmaxyx(stdscr)
    settings_manager = SettingsManager()
    sound_manager = SoundManager()
    
    options = [
        "Sound Effects: {}",
        "Background Music: {}",
        "Sound Volume: {}%",
        "Music Volume: {}%",
        "Back"
    ]
    current_row = 0
    
    while True:
        unicurses.clear()
        
        # Update option texts with current settings
        options[0] = options[0].format("ON" if settings_manager.get_setting("sound_enabled") else "OFF")
        options[1] = options[1].format("ON" if settings_manager.get_setting("music_enabled") else "OFF")
        options[2] = options[2].format(int(settings_manager.get_setting("sound_volume") * 100))
        options[3] = options[3].format(int(settings_manager.get_setting("music_volume") * 100))
        
        # Draw title
        title = "Settings (Use ← → to change values)"
        unicurses.move(sh//4, sw//2 - len(title)//2)
        unicurses.addstr(title)
        
        # Draw options
        for idx, option in enumerate(options):
            y = sh//4 + idx + 2
            x = sw//2 - len(option)//2
            unicurses.move(y, x)
            if idx == current_row:
                unicurses.attron(unicurses.A_REVERSE)
            unicurses.addstr(option)
            if idx == current_row:
                unicurses.attroff(unicurses.A_REVERSE)
        
        unicurses.refresh()
        
        key = unicurses.getch()
        if key == unicurses.KEY_UP and current_row > 0:
            current_row -= 1
            sound_manager.play_menu_sound()
        elif key == unicurses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
            sound_manager.play_menu_sound()
        elif key == unicurses.KEY_LEFT or key == unicurses.KEY_RIGHT:
            if current_row < 4:  # Not on "Back" option
                sound_manager.play_menu_sound()
                if current_row == 0:  # Sound Effects toggle
                    new_value = not settings_manager.get_setting("sound_enabled")
                    settings_manager.set_setting("sound_enabled", new_value)
                elif current_row == 1:  # Background Music toggle
                    new_value = not settings_manager.get_setting("music_enabled")
                    settings_manager.set_setting("music_enabled", new_value)
                    if new_value:
                        sound_manager.start_background_music()
                    else:
                        sound_manager.stop_background_music()
                elif current_row == 2:  # Sound Volume
                    volume = settings_manager.get_setting("sound_volume")
                    if key == unicurses.KEY_RIGHT:
                        volume = min(1.0, volume + 0.1)
                    else:
                        volume = max(0.0, volume - 0.1)
                    settings_manager.set_setting("sound_volume", volume)
                elif current_row == 3:  # Music Volume
                    volume = settings_manager.get_setting("music_volume")
                    if key == unicurses.KEY_RIGHT:
                        volume = min(1.0, volume + 0.1)
                    else:
                        volume = max(0.0, volume - 0.1)
                    settings_manager.set_setting("music_volume", volume)
                    if settings_manager.get_setting("music_enabled"):
                        sound_manager.stop_background_music()
                        sound_manager.start_background_music()
        elif key in [unicurses.KEY_ENTER, 10, 13] and current_row == 4:  # Back option
            return
        elif key == 27:  # Escape
            return

def draw_menu(stdscr):
    sh, sw = unicurses.getmaxyx(stdscr)
    menu = ["Start Game", "Create Player", "Select Player", "Settings", "Exit"]
    current_row = 0
    sound_manager = SoundManager()

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
            sound_manager.play_menu_sound()
        elif key == unicurses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
            sound_manager.play_menu_sound()
        elif key in [unicurses.KEY_ENTER, 10, 13]:
            choice = menu[current_row].lower().replace(" ", "_")
            if choice == "settings":
                settings_menu(stdscr)
            else:
                return choice

def draw_pause_menu(buffer):
    """Draw the pause menu with options."""
    sh, sw = unicurses.getmaxyx(buffer)
    menu = ["Resume", "Main Menu"]
    current_row = 0
    sound_manager = SoundManager()

    # Clear the buffer once at the start
    unicurses.werase(buffer)
    
    while True:
        # Draw title
        title = "GAME PAUSED"
        unicurses.mvwaddstr(buffer, sh // 3, sw // 2 - len(title) // 2, title)

        # Draw menu options
        for idx, row in enumerate(menu):
            x = sw // 2 - len(row) // 2
            y = sh // 2 - len(menu) // 2 + idx
            if idx == current_row:
                unicurses.wattrset(buffer, unicurses.A_REVERSE)
                unicurses.mvwaddstr(buffer, y, x, row)
                unicurses.wattrset(buffer, unicurses.A_NORMAL)
            else:
                unicurses.mvwaddstr(buffer, y, x, row)

        # Use double buffering to prevent flickering
        unicurses.wnoutrefresh(buffer)
        unicurses.doupdate()

        key = unicurses.wgetch(buffer)
        if key == unicurses.KEY_UP and current_row > 0:
            current_row -= 1
            sound_manager.play_menu_sound()
        elif key == unicurses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
            sound_manager.play_menu_sound()
        elif key in [unicurses.KEY_ENTER, 10, 13]:
            if current_row == 0:  # Resume
                return "resume"
            else:  # Main Menu
                return "main_menu"
        elif key == 27:  # Escape key
            return "resume"

def generate_planets():
    planets = []
    moons = []
    planet_data = Planet.load_planets()
    
    # Create planets with data from planets.json
    for data in planet_data:
        x = data.get('position', {}).get('x', random.randint(0, WORLD_WIDTH - 1))
        y = data.get('position', {}).get('y', random.randint(0, WORLD_HEIGHT - 1))
        size = data.get('size', random.randint(1, 3))
        planets.append(Planet(x, y, size, data))
    
    # Create additional random planets if needed
    while len(planets) < NUM_PLANETS:
        x = random.randint(0, WORLD_WIDTH - 1)
        y = random.randint(0, WORLD_HEIGHT - 1)
        size = random.randint(1, 3)
        planets.append(Planet(x, y, size))

    # Generate moons for planets
    for planet in planets:
        for _ in range(random.randint(0, NUM_MOONS_PER_PLANET)):
            moon = Moon(planet.x, planet.y, random.randint(3, MOON_ORBIT_RADIUS))
            moons.append(moon)
            
    return planets, moons

def generate_asteroids(num_asteroids, sw):
    return [Asteroid(random.randint(0, WORLD_WIDTH - 1), 0) for _ in range(num_asteroids)]

def draw_world(buffer, player, planets, moons, asteroids):
    sh, sw = unicurses.getmaxyx(buffer)
    top = max(0, player.position["y"] - sh // 2)
    left = max(0, player.position["x"] - sw // 2)

    # Clear the buffer and reset attributes
    unicurses.werase(buffer)
    unicurses.wattrset(buffer, unicurses.color_pair(3))  # Reset to default white

    # Draw borders
    for y in range(sh):
        screen_x_left = 0 - left
        screen_x_right = WORLD_WIDTH - 1 - left
        if 0 <= screen_x_left < sw:
            unicurses.mvwaddch(buffer, y, screen_x_left, ord('#'))
        if 0 <= screen_x_right < sw:
            unicurses.mvwaddch(buffer, y, screen_x_right, ord('#'))
    
    for x in range(sw):
        screen_y_top = 0 - top
        screen_y_bottom = WORLD_HEIGHT - 1 - top
        if 0 <= screen_y_top < sh:
            unicurses.mvwaddch(buffer, screen_y_top, x, ord('#'))
        if 0 <= screen_y_bottom < sh:
            unicurses.mvwaddch(buffer, screen_y_bottom, x, ord('#'))

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
    for planet in planets:
        if top <= planet.y < top + sh and left <= planet.x < left + sw:
            screen_y = planet.y - top
            screen_x = planet.x - left
            if 0 <= screen_y < sh and 0 <= screen_x < sw:
                planet_symbol = planet.get_symbol().split('\n')
                for i, line in enumerate(planet_symbol):
                    if 0 <= screen_y + i < sh:
                        unicurses.mvwaddstr(buffer, screen_y + i, screen_x, line)
    
    # Draw moons
    for moon in moons:
        if top <= moon.y < top + sh and left <= moon.x < left + sw:
            screen_y = moon.y - top
            screen_x = moon.x - left
            if 0 <= screen_y < sh and 0 <= screen_x < sw:
                unicurses.mvwaddstr(buffer, screen_y, screen_x, 'o')
    
    # Draw asteroids
    for asteroid in asteroids:
        if asteroid.visible and top <= asteroid.y < top + sh and left <= asteroid.x < left + sw:
            unicurses.mvwaddch(buffer, asteroid.y - top, asteroid.x - left, ord('X'))

    # Draw player with direction and health-based character
    player_chars = {
        'up': '▲' if player.health >= 50 else '△',
        'down': '▼' if player.health >= 50 else '▽',
        'left': '◄' if player.health >= 50 else '◁',
        'right': '►' if player.health >= 50 else '▷'
    }
    player_char = player_chars.get(player.direction, '▲')  # Default to up arrow if direction is unknown
    unicurses.mvwaddwstr(buffer, player.position["y"] - top, player.position["x"] - left, player_char)

    # Refresh the buffer
    unicurses.wnoutrefresh(buffer)
    unicurses.doupdate()

def is_collision_with_planet(x, y, planets):
    for planet in planets:
        # Calculate distance between point and planet center using Pythagorean theorem
        distance = ((planet.x - x) ** 2 + (planet.y - y) ** 2) ** 0.5
        if distance <= planet.size:  # If distance is less than or equal to planet radius
            return True
    return False

def game_loop(buffer, player, planets, moons, sh, sw):
    # Game settings
    ASTEROID_SPEED = 15.0  # positions per second
    ASTEROID_FREQUENCY = 5  # new asteroids per second
    FUEL_REGEN_TIME = 10.0  # seconds to wait before regenerating fuel
    FUEL_REGEN_AMOUNT = 15  # amount of fuel to regenerate
    REFRESH_RATE = 0.05  # seconds between screen refreshes
    
    sound_manager = SoundManager()  # Initialize sound manager
    sound_manager.play_background_music()  # Start with a random track
    
    last_move_time = time.time()
    last_asteroid_time = time.time()
    last_movement_time = time.time()  # Track when player last moved
    last_refresh_time = time.time()   # Track when screen was last refreshed
    accumulated_movement = 0.0

    # Set input to non-blocking
    unicurses.nodelay(buffer, True)

    # Create buffer window for double buffering
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
            elif key == 27:  # Escape key
                unicurses.nodelay(buffer, False)  # Set to blocking input for menu
                choice = draw_pause_menu(buffer)
                if choice == "main_menu":
                    return "main_menu"
                unicurses.nodelay(buffer, True)  # Set back to non-blocking
                last_refresh_time = time.time()  # Reset timers
                continue

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
            save_player_fuel(player)
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
                    save_player_fuel(player)
                    return

        # Remove invisible asteroids
        asteroids = [ast for ast in asteroids if ast.visible]

        # Update moon positions
        for moon in moons:
            moon.move()

        # Check if we need to play the next music track
        sound_manager.check_and_play_next_track()

        # Update screen at regular intervals
        if current_time - last_refresh_time >= REFRESH_RATE:
            draw_world(buffer, player, planets, moons, asteroids)
            last_refresh_time = current_time

        # Small sleep to prevent CPU overuse
        time.sleep(0.01)

def save_player_fuel(player):
    players = load_players()
    for p in players:
        if p["name"] == player.name:
            p["inventory"]["fuel"] = player.fuel
            break
    save_players(players)

def main(stdscr):
    import locale
    locale.setlocale(locale.LC_ALL, '')
    
    unicurses.curs_set(0)
    unicurses.start_color()
    unicurses.init_pair(1, unicurses.COLOR_RED, unicurses.COLOR_BLACK)    # For critical levels (<30%)
    unicurses.init_pair(2, unicurses.COLOR_YELLOW, unicurses.COLOR_BLACK) # For warning levels (<50%)
    unicurses.init_pair(3, unicurses.COLOR_WHITE, unicurses.COLOR_BLACK)  # For normal levels
    sh, sw = unicurses.getmaxyx(stdscr)
    unicurses.keypad(stdscr, True)

    current_player_id = None
    current_player_name = None
    sound_manager = SoundManager()

    while True:
        choice = draw_menu(stdscr)
        if choice == "start_game":
            if current_player_id:
                # Start background music when game starts
                sound_manager.play_background_music()
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

    # Generate random planets and moons
    planets, moons = generate_planets()

    # Start the game loop
    while True:
        result = game_loop(buffer, player, planets, moons, sh, sw)
        if result == "main_menu":
            # Stop background music
            sound_manager.stop_background_music()
            # Clear the screen
            unicurses.clear()
            unicurses.refresh()
            # Reset to blocking input for menu
            unicurses.nodelay(stdscr, False)
            return main(stdscr)  # Restart from main menu
        else:
            break
    
    # Stop background music when game ends
    sound_manager.stop_background_music()

if __name__ == "__main__":
    unicurses.wrapper(main)