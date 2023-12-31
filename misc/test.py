import curses

COLOR_PAIRS_CACHE = {}


def _get_color(fg, bg):
    key = (fg, bg)
    if key not in COLOR_PAIRS_CACHE:
        # Use the pairs from 101 and after, so there's less chance they'll be overwritten by the user
        pair_num = len(COLOR_PAIRS_CACHE) + 1
        curses.init_pair(pair_num, fg, bg)
        COLOR_PAIRS_CACHE[key] = pair_num

    return COLOR_PAIRS_CACHE[key]


def run(stdscr):
    curses.start_color()
    curses.use_default_colors()

    count = 0
    for y in range(16):
        for x in range(16):
            stdscr.addstr(y, x+(x*4), str(count), curses.color_pair(_get_color(count, -1)))
            count += 1

    stdscr.getch()

curses.wrapper(run)