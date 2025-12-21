import os, json
import cv2, webview
from pose_checker import check_frame
from settings import *


MAIN_MENU, SETTINGS, HELP, GAME_SETUP, ROUND_SHOW_POSE, ROUND_TIMER, ROUND_SHOW_SCORE, TOTAL_RATING, QUIT, NULL = range(10)


class Api:
    def close(self) -> None:
        window.destroy() # type: ignore
    

    def get_frame(self):
        if cap.isOpened():
            success, frame = cap.read()
            if success:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return cv2.imread(VIDEO_PLACEHOLDER)
    

    def submit(self, formHTML) -> None:
        action = os.path.basename(formHTML["action"])
        values = {}
        for node in formHTML["childNodes"]:
            if node["nodeName"] == "INPUT":
                values[node["name"]] = node["value"]
        getattr(self, action)(values)
    

    def save(self, values: dict) -> None:
        json.dump(values, open(SETTINGS_PATH, "wt"))


def setup() -> None:
    global window, cap
    window = webview.create_window('Woah dude!', 'pages/main.html', js_api=Api(), fullscreen=True)
    try:
        cap = cv2.VideoCapture(1)
    except:
        cap = cv2.VideoCapture()


if __name__ == "__main__":
    setup()
    webview.start()