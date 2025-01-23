# FILE: game.py
import unicurses
import random
import time

import json
import uuid
WORLD_WIDTH = 100
WORLD_HEIGHT = 100
NUM_PLANETS = 10
NUM_ASTEROIDS = 20  # Increased number of asteroids
ASTEROID_SPEED = 30.0  # Increased speed of asteroids

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

def draw_world(buffer, player_x, player_y, planets, asteroids, life):
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

    # Draw life score
    unicurses.mvwaddstr(buffer, 0, 0, f"Life: {life}")

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

    # Game settings
    last_move_time = time.time()
    accumulated_movement = 0.0

    # Player life
    life = 100

    # Generate random planets
    planets = generate_planets()

    # Generate random asteroids
    asteroids = generate_asteroids(NUM_ASTEROIDS, sw)

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

        # Continuously generate new asteroids
        while len(asteroids) < NUM_ASTEROIDS:
            asteroids.append((random.randint(0, WORLD_WIDTH - 1), 0))

        # Check for collision with planets
        asteroids = [(ax, ay) for ax, ay in asteroids if not is_collision_with_planet(ax, ay, planets)]

        # Check for collision with player
        if (player_x, player_y) in asteroids:
            life -= 25

        if life <= 0:  # Change the condition to <= 0
            unicurses.clear()
            unicurses.move(sh // 2, sw // 2 - len("Game Over!") // 2)
            unicurses.addstr("Game Over!")
            unicurses.refresh()
            unicurses.napms(2000)
            break

        draw_world(buffer, player_x, player_y, planets, asteroids, life)

if __name__ == "__main__":
    unicurses.wrapper(main)