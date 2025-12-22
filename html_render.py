import os, json, random
import cv2, webview
from pose_checker import *
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
    

    def round(self) -> None:
        self.pose = random.randint(1, POSES_COUNT)
        js = f"""
            const poseElement = document.getElementById("pose");
            poseElement.src = "poses/{self.pose:02d}.jpg";
            contst timerElement = document.getElementById("timer");
            var timer = {settings["timer"]};
            const interval = setInterval(() => {{
                timer.innerText = timer;
                timer--;
                if (timer == 0) {{
                    clearInterval(interval);
                    window.pywebview.api.check_poses();
                }}
            }}, 1000);
        """
        window.run_js(js) # type: ignore
    

    def rating(self) -> None:
        pass
    

    def check_poses(self) -> None:
        while not cap.isOpened():
            pass
        success = False
        while not success:
            success, frame = cap.read()
        self.check_result = check_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), self.pose) # type: ignore
        window.load_url("pages/rating.html") # type: ignore


def setup() -> None:
    global window, cap, settings
    window = webview.create_window('Woah dude!', 'pages/main.html', js_api=Api(), fullscreen=True)
    try:
        cap = cv2.VideoCapture(1)
    except:
        cap = cv2.VideoCapture()
    settings = json.load(open(SETTINGS_PATH, 'rt'))


if __name__ == "__main__":
    setup()
    webview.start()