import cv2
import mediapipe as mp
from pose_checker import *
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

angles = json.load(open(os.path.sep.join((SAMPLES_PATH, f"{1:02d}.json"))))

cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
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
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        prev = int(image.shape[0] / 2), int(image.shape[1] / 2)
        length = 100
        for angle in angles[:4]:
            point = int(prev[0] + length * math.cos(angle)), int(prev[1] - length * math.sin(angle))
            cv2.line(image, prev, point, (0, 0, 0), 3)
            prev = point
        if results is not None and results.pose_landmarks is not None and results.pose_landmarks.landmark is not None:
            conf = check_id([(landmark.x, landmark.y) for landmark in results.pose_landmarks.landmark], 1)
            cv2.putText(image, f"{conf:.4f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255 * conf, 255 * (1 - conf)), 3)
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()