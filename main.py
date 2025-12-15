from settings import *


MAIN_MENU, SETTINGS, HELP, GAME_SETUP, ROUND_SHOW_POSE, ROUND_TIMER, ROUND_SHOW_SCORE, TOTAL_RATING, QUIT = range(9)


def main() -> None:
    global status
    status = MAIN_MENU
    while status != QUIT:
        if status == MAIN_MENU:
            pass
        elif status == SETTINGS:
            pass
        elif status == HELP:
            pass
        elif status == GAME_SETUP:
            pass
        elif status == ROUND_SHOW_POSE:
            pass
        elif status == ROUND_TIMER:
            pass
        elif status == ROUND_SHOW_SCORE:
            pass
        elif status == TOTAL_RATING:
            pass


if __name__ == "__main__":
    main()