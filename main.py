import os, json, random
import cv2, webview, base64, numpy as np
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
        global settings
        json.dump(values, open(SETTINGS_PATH, "wt"))
        settings = values
    

    def round(self) -> None:
        if not hasattr(self, "round_counter") or self.round_counter == 0:
            self.round_counter = settings["rounds"]
        self.round_counter -= 1
        self.pose = random.randint(1, POSES_COUNT)
        js = f"""
            const poseElement = document.getElementById("pose");
            poseElement.src = "poses/{self.pose:02d}.jpg";
            const timerElement = document.getElementById("timer");
            var timer = {settings["timer"]};
            const interval = setInterval(async () => {{
                if (timer == 0) {{
                    clearInterval(interval);
                    await window.pywebview.api.check_frame(grabFrame());
                    {"window.location.href = 'rating.html';" if self.round_counter == 0 else "window.location.reload();"}
                }}
                timerElement.innerText = timer;
                timer--;
            }}, 1000);
        """
        window.run_js(js) # type: ignore
    

    def settings(self) -> None:
        js = f"""
            const param1Element = document.getElementById("param1");
            const param2Element = document.getElementById("param2");
            param1Element.value = {settings["timer"]};
            param2Element.value = {settings["rounds"]};
        """
        window.run_js(js) # type: ignore
    

    def check_frame(self, frame_url: str) -> None:
        encoded = frame_url.split(',')[1]
        img_bytes = base64.b64decode(encoded)
        frame = cv2.imdecode(
            np.frombuffer(img_bytes, np.uint8),
            cv2.IMREAD_COLOR
        )
        if not hasattr(self, "check_results"):
            self.check_results = []
        self.check_results.append(check_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), self.pose)) # type: ignore
    

    def rating(self) -> None:
        if len(self.check_results) == 0:
            self.check_results = [0]
        js = f"""
            const scoreElement = document.getElementById("score");
            scoreElement.innerText = {sum(self.check_results) / len(self.check_results) * 100:.0f} + "%";
        """
        window.run_js(js) # type: ignore
        self.check_results = []


def debug_js(js: str) -> None:
    result = window.evaluate_js( # type: ignore
    f"""
        (() => try {{ {js}\nreturn {{ok: true}} }} catch (e) {{ return {{ok: false, message: e.message, stack: e.stack}} }})
    """)
    if not result["ok"]:
        raise Exception(result["message"], result["stack"])


def setup() -> None:
    global window, settings
    window = webview.create_window('GUI', 'pages/main.html', js_api=Api(), fullscreen=True)
    settings = json.load(open(SETTINGS_PATH, 'rt'))


if __name__ == "__main__":
    setup()
    webview.start()