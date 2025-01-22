# FILE: game.py
import unicurses

def main(stdscr):
    # Clear screen
    unicurses.curs_set(0)
    unicurses.nodelay(stdscr, True)
    unicurses.timeout(100)

    sh, sw = unicurses.getmaxyx(stdscr)
    w = stdscr
    unicurses.keypad(w, True)

    # Initial position of the player
    x, y = sw // 2, sh // 2
    unicurses.mvwaddch(w, y, x, '@')

    while True:
        key = unicurses.wgetch(w)

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

        unicurses.wclear(w)
        unicurses.mvwaddch(w, y, x, '@')
        unicurses.wrefresh(w)

if __name__ == "__main__":
    unicurses.wrapper(main)