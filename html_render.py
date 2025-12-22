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
            const timerElement = document.getElementById("timer");
            var timer = {settings["timer"]};
            const interval = setInterval(() => {{
                if (timer == 0) {{
                    clearInterval(interval);
                    window.location.href = "rating.html";
                }}
                timerElement.innerText = timer;
                timer--;
            }}, 1000);
        """
        window.run_js(js) # type: ignore
    

    def rating(self) -> None:
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        if cap.isOpened():
            success, frame = cap.read()
            if success:
                self.check_result = check_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), self.pose) # type: ignore
            else:
                self.check_result = 0
        else:
            self.check_result = 0
        js = f"""
            const tableElement = document.getElementById("rtable");
            const rowElement = document.createElement("tr");
            const nameElement = document.createElement("td");
            const scoreElement = document.createElement("td");
            nameElement.innerText = "Player 1";
            scoreElement.innerText = {self.check_result * MAX_SCORE:.0f};
            rowElement.appendChild(nameElement);
            rowElement.appendChild(scoreElement);
            tableElement.appendChild(rowElement);
        """
        window.run_js(js) # type: ignore


def setup() -> None:
    global window, settings
    window = webview.create_window('Woah dude!', 'pages/main.html', js_api=Api(), fullscreen=True)
    settings = json.load(open(SETTINGS_PATH, 'rt'))


if __name__ == "__main__":
    setup()
    webview.start()