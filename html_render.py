import os, json
import cv2, webview
from settings import *


class Api:
    def close(self) -> None:
        window.destroy() # type: ignore
    

    def submit(self, formHTML) -> None:
        action = os.path.basename(formHTML["action"])
        values = {}
        for node in formHTML["childNodes"]:
            if node["nodeName"] == "INPUT":
                values[node["name"]] = node["value"]
        try:
            getattr(self, action)(values)
        except AttributeError:
            return
    

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