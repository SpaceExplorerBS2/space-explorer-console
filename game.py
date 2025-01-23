# FILE: game.py
import unicurses
import random

def draw_menu(stdscr):
    sh, sw = unicurses.getmaxyx(stdscr)
    menu = ["Start", "Exit"]
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
            if current_row == 0:
                return "start"
            elif current_row == 1:
                return "exit"

def main(stdscr):
    # Clear screen
    unicurses.curs_set(0)
    sh, sw = unicurses.getmaxyx(stdscr)
    unicurses.keypad(stdscr, True)

    while True:
        choice = draw_menu(stdscr)
        if choice == "start":
            break
        elif choice == "exit":
            return

    unicurses.nodelay(stdscr, True)
    unicurses.timeout(100)

    # Initial position of the player
    x, y = sw // 2, sh // 2
    unicurses.move(y, x)
    unicurses.addch('@')

    # Generate random asteroids
    asteroids = [(random.randint(0, sw - 1), 0) for _ in range(5)]

    while True:
        key = unicurses.getch()

        if key == unicurses.KEY_UP:
            y = max(0, y - 1)
        elif key == unicurses.KEY_DOWN:
            y = min(sh - 1, y + 1)
        elif key == unicurses.KEY_LEFT:
            x = max(0, x - 1)
        elif key == unicurses.KEY_RIGHT:
            x = min(sw - 1, x + 1)
        elif key == ord('q'):
            break

        # Move asteroids down
        new_asteroids = []
        for ax, ay in asteroids:
            if ay < sh - 1:
                new_asteroids.append((ax, ay + 1))
            else:
                new_asteroids.append((random.randint(0, sw - 1), 0))
        asteroids = new_asteroids

        # Check for collision
        if (x, y) in asteroids:
            unicurses.clear()
            unicurses.move(sh // 2, sw // 2 - len("Game Over!") // 2)
            unicurses.addstr("Game Over!")
            unicurses.refresh()
            unicurses.napms(2000)
            break

        unicurses.clear()
        unicurses.move(y, x)
        unicurses.addch('@')

        for ax, ay in asteroids:
            unicurses.move(ay, ax)
            unicurses.addch('X')

        unicurses.refresh()

if __name__ == "__main__":
    unicurses.wrapper(main)