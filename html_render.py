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
                if node["type"] == "number":
                    values[node["name"]] = node["valueAsNumber"]
                else:
                    values[node["name"]] = node["value"]
        try:
            getattr(self, action)(values)
        except AttributeError:
            return
    

    def save(self, values: dict) -> None:
        json.dump(values, open(SETTINGS_PATH, "wt"))
    

    def get_settings(self):
        return json.load(open(SETTINGS_PATH, 'rt'))


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