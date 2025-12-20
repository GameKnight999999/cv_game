import random
from settings import *
import ui_facade as ui


MAIN_MENU, SETTINGS, HELP, GAME_SETUP, ROUND_SHOW_POSE, ROUND_TIMER, ROUND_SHOW_SCORE, TOTAL_RATING, QUIT, NULL = range(10)

def test():
    ui.play_sound('boop')
'''
def mental_help() -> None:
    ui.clearscreen()
    ui.Image.load('test.png', 100, 100)
    ui.Button("hewwo :3", lambda: test(), 200, 800, 200, 100)
'''
def help() -> None:
    ui.clearscreen()
    ui.Button("follow the pose of the", lambda: test(), 200, 100, 200, 100)
    ui.Button("little guy on the screen", lambda: test(), 200, 200, 200, 100)
    ui.Button("as precise as you can", lambda: test(), 200, 300, 200, 100)
    ui.Button("to get more points and ", lambda: test(), 200, 400, 200, 100)
    ui.Button("win the round!", lambda: test(), 200, 500, 200, 100)
    ui.Button("go back", lambda: globals().__setitem__("event", MAIN_MENU), 500, 800, 200, 100)


def main_menu() -> None:
    ui.clearscreen()
    ui.Image.load(MAIN_MENU_BACKGROUND, 0, 0)
    ui.Button("Start game", lambda: globals().__setitem__("event", GAME_SETUP), 50, 50, 200, 100)
    ui.Button("Quit", lambda: globals().__setitem__("event", QUIT), 50, 200, 200, 100)
    ui.Button("Settings", lambda: globals().__setitem__("event", SETTINGS), 50, 350, 200, 100)
    ui.Button("(mental) Help", lambda: globals().__setitem__("event", HELP), 50, 500, 200, 100)
    ui.play_music('test')


def main() -> None:
    global event
    event = MAIN_MENU
    while event != QUIT:
        if event == MAIN_MENU:
            main_menu()
        elif event == SETTINGS:
            pass
        elif event == HELP:
            help()
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