# FILE: game.py
import unicurses

def draw_menu(stdscr):
    sh, sw = unicurses.getmaxyx(stdscr)
    menu = ["Start", "Exit"]
    current_row = 0

    while True:
        stdscr.clear()
        for idx, row in enumerate(menu):
            x = sw // 2 - len(row) // 2
            y = sh // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.attron(unicurses.A_REVERSE)
                stdscr.addstr(y, x, row)
                stdscr.attroff(unicurses.A_REVERSE)
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()

        key = stdscr.getch()

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
    stdscr.timeout(100)

    # Initial position of the player
    x, y = sw // 2, sh // 2
    stdscr.addch(y, x, '@')

    while True:
        key = stdscr.getch()

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

        stdscr.clear()
        stdscr.addch(y, x, '@')
        stdscr.refresh()

if __name__ == "__main__":
    unicurses.wrapper(main)