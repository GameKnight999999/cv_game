from random import randint
import pygame
import cv2

import event_handler
from pose_checker import *
import mediapipe as mp
import settings
import ui_facade as ui

MAIN_MENU, SETTINGS, HELP, GAME_SETUP, ROUND_SHOW_POSE, ROUND_SHOW_SCORE, TOTAL_RATING, QUIT, NULL = range(9)
music_playing = False
countdown_playing = False
zero_playing = False
score = []
font = ui.Font()
round_num = 0
round_score = 0
cap = None

def test():
    ui.play_sound('boop')

def help() -> None:
    ui.clearscreen()
    ui.Button("follow the pose of the", lambda: test(), 200, 100, False)
    ui.Button("little guy on the screen", lambda: test(), 200, 200, False)
    ui.Button("as precise as you can", lambda: test(), 200, 300, False)
    ui.Button("to get more points and ", lambda: test(), 200, 400, False)
    ui.Button("win the round!", lambda: test(), 200, 500, False)
    ui.Button("m to mute, esc to quit", lambda: test(), 200, 650, False)
    ui.Button("go back", lambda: globals().__setitem__("event", MAIN_MENU), 500, 800, True)

def draw_settings():
    ui.clearscreen()
    ui.ButtonArrows('volume:', 'USER_VOLUME', settings.USER_VOLUME, 100, 50, 50, tuple(), 10, 0)
    ui.ButtonArrows('timer value:', 'TIMER', settings.TIMER, 60, 50, 200)
    ui.ButtonArrows('mod:', 'MOD', settings.MOD, 0, 50, 350, settings.MODS)
    ui.ButtonArrows('theme:', 'THEME', settings.THEME, 0, 50, 500, settings.THEMES)
    ui.Button("done", lambda: globals().__setitem__("event", MAIN_MENU), 500, 800, True)
    if settings.HIGH_SCORE:
        ui.Label(f'high score: {settings.HIGH_SCORE}', settings.FONT_SIZE, 50, 650)


def main_menu() -> None:
    global music_playing
    ui.clearscreen()
    if settings.THEME == 'dark':
        ui.Image.load('main_background_dark.png', 0, 0)
    else:
        ui.Image.load('main_background_light.png', 0, 0)
    ui.Button("Start game", lambda: globals().__setitem__("event", GAME_SETUP), 50, 50, True)
    ui.Button("Quit", lambda: globals().__setitem__("event", QUIT), 50, 200, True)
    ui.Button("Settings", lambda: globals().__setitem__("event", SETTINGS), 50, 350, True)
    ui.Button("Help", lambda: globals().__setitem__("event", HELP), 50, 500, True)
    if not music_playing:
        ui.play_music('test')
        music_playing = True

def game_setup():
    ui.clearscreen()
    ui.ButtonArrows('number of players:', 'PLAYERS', settings.PLAYERS, settings.MAX_PLAYERS, 50, 50)
    if settings.MOD == 'rounds':
        ui.ButtonArrows('number of rounds:', 'ROUNDS', settings.ROUNDS, settings.MAX_ROUNDS, 50, 300)
    elif settings.MOD == 'score':
        ui.ButtonArrows('target score:', 'TARGET_SCORE', settings.TARGET_SCORE, settings.MAX_TARGET_SCORE, 50, 350, tuple(), 100)
    ui.Button("continue", lambda: globals().__setitem__("event", ROUND_SHOW_POSE), 500, 800, True)

def draw_timer():
    global round_num, countdown_playing, zero_playing
    if font.timer_running:
        elapsed = pygame.time.get_ticks() // 1000 - font.timer_start_time
        remaining = settings.TIMER - elapsed
        if remaining == 5 and not countdown_playing:
            ui.play_sound('countdown_v2')
            countdown_playing = True
        if remaining == 0 and not zero_playing:
            ui.play_sound('countdown_v1')
            zero_playing = True
        elif remaining < 0:
            font.end_timer()
            countdown_playing = False
            zero_playing = False
            return
        ui.Font.print_at(font, str(remaining), settings.FONT_SIZE, 600, 150)

def show_round_stats():
    global round_num, score
    ui.clearscreen()
    ui.Label(f'round: {round_num}', settings.FONT_SIZE, 100, 100)
    ui.Label(f'score in this round: {score[-1]}', settings.FONT_SIZE, 100, 250)
    ui.Label(f'total score: {sum(score)}', settings.FONT_SIZE, 100, 400)
    if settings.MOD == 'score':
        ui.Label(f'score left until target: {settings.TARGET_SCORE - sum(score)}', settings.FONT_SIZE, 100, 550)
    ui.Button('continue', lambda: globals().__setitem__("event", ROUND_SHOW_POSE), 500, 800, True)

def show_round_results():
    global round_num, score
    ui.clearscreen()
    if sum(score) >= settings.HIGH_SCORE:
        settings.HIGH_SCORE = sum(score)
    ui.Label(f'rounds played: {round_num}', settings.FONT_SIZE, 400, 100)
    ui.Label(f'total score: {sum(score)}', settings.FONT_SIZE, 400, 300)
    ui.Label(f'high score: {settings.HIGH_SCORE}', settings.FONT_SIZE, 400, 500)
    ui.Button('exit', lambda: globals().__setitem__("event", MAIN_MENU), 500, 800, True)

def show_round():
    global round_score, round_num
    round_num += 1
    ui.clearscreen()
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    angles = json.load(open(os.path.sep.join((SAMPLES_PATH, f"{1:02d}.json"))))
    pose_id = randint(1, 13)

    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
    ) as pose:

        font.start_timer(settings.TIMER)
        font.timer_start_time = pygame.time.get_ticks() // 1000
        while font.timer_running:
            event_handler.tick()
            ui.clearscreen()
            draw_timer()
            ui.Font.print_at(font, f'round: {round_num}', settings.FONT_SIZE, 500, 50)
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.flip(image, 1)

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

            pose_img = cv2.imread(os.path.sep.join((SAMPLES_PATH, f"{pose_id:02d}.jpg")))
            # picture's width and height is adjusted here
            pose_img = cv2.resize(pose_img, None, fx=1 / 3, fy=1 / 3)
            # image[image.shape[0] - pose_img.shape[0]:, :pose_img.shape[1]] = pose_img
            image[:pose_img.shape[0], image.shape[1] - pose_img.shape[1]:] = pose_img

            if results and results.pose_landmarks and results.pose_landmarks.landmark:
                conf = check_id(
                    [(lm.x, lm.y) for lm in results.pose_landmarks.landmark],
                    pose_id
                )
                cv2.putText(
                    image,
                    f"{conf:.4f}",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255 * conf, 255 * (1 - conf)),
                    3
                )
                round_score = round(float(f"{conf:.4f}") * settings.MAX_SCORE)

            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            frame = frame.swapaxes(0, 1)
            surface = pygame.surfarray.make_surface(frame)
            ui.screen.blit(surface, (0, 250))
            pygame.display.flip()
        if settings.MOD == 'rounds':
            if round_num < settings.ROUNDS:
                score.append(round_score)
                globals().__setitem__("event", ROUND_SHOW_SCORE)
            elif round_num == settings.ROUNDS:
                score.append(round_score)
                globals().__setitem__("event", TOTAL_RATING)
        elif settings.MOD == 'score':
            if sum(score) + round_score < settings.TARGET_SCORE:
                score.append(round_score)
                globals().__setitem__("event", ROUND_SHOW_SCORE)
            elif sum(score) + round_score >= settings.TARGET_SCORE:
                score.append(round_score)
                globals().__setitem__("event", TOTAL_RATING)


def main() -> None:
    global event, cap
    event = MAIN_MENU
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while event != QUIT:
        if event == MAIN_MENU:
            main_menu()
        elif event == SETTINGS:
            draw_settings()
        elif event == HELP:
            help()
        elif event == GAME_SETUP:
            game_setup()
        elif event == ROUND_SHOW_POSE:
            show_round()
        elif event == ROUND_SHOW_SCORE:
            show_round_stats()
        elif event == TOTAL_RATING:
            show_round_results()
        ui.tick()
    if cap is not None:
        cap.release()
    pygame.quit()

if __name__ == "__main__":
    main()