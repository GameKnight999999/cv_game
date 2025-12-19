from settings import *
import ui_facade as ui


MAIN_MENU, SETTINGS, HELP, GAME_SETUP, ROUND_SHOW_POSE, ROUND_TIMER, ROUND_SHOW_SCORE, TOTAL_RATING, QUIT, NULL = range(10)


def clearscreen() -> None:
    ui.ui_elements = []


def main_menu() -> None:
    clearscreen()
    ui.Image.load(MAIN_MENU_BACKGROUND, 0, 0)
    ui.Button("Start game", lambda: setattr(globals(), "event", GAME_SETUP), 50, 50, 200, 100)
    ui.Button("Quit", lambda: setattr(globals(), "event", QUIT), 300, 50, 200, 100)
    ui.Button("Settings", lambda: setattr(globals(), "event", SETTINGS), 550, 50, 200, 100)
    ui.Button("Help", lambda: setattr(globals(), "event", HELP), 800, 50, 200, 100)
    


def main() -> None:
    global event
    event = MAIN_MENU
    while event != QUIT:
        if event == MAIN_MENU:
            main_menu()
        elif event == SETTINGS:
            pass
        elif event == HELP:
            pass
        elif event == GAME_SETUP:
            pass
        elif event == ROUND_SHOW_POSE:
            pass
        elif event == ROUND_TIMER:
            pass
        elif event == ROUND_SHOW_SCORE:
            pass
        elif event == TOTAL_RATING:
            pass
        event = NULL
        ui.tick()


if __name__ == "__main__":
    main()