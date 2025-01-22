# FILE: game.py
import curses

def main(stdscr):
    # Clear screen
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)

    # Initial position of the player
    x, y = sw // 2, sh // 2
    w.addch(y, x, '@')

    while True:
        key = w.getch()

        if key == curses.KEY_UP:
            y = max(0, y - 1)
        elif key == curses.KEY_DOWN:
            y = min(sh - 1, y + 1)
        elif key == curses.KEY_LEFT:
            x = max(0, x - 1)
        elif key == curses.KEY_RIGHT:
            x = min(sw - 1, x + 1)
        elif key == ord('q'):
            break

        w.clear()
        w.addch(y, x, '@')
        w.refresh()

if __name__ == "__main__":
    curses.wrapper(main)