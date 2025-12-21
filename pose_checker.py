"""
    Some functions for pose checking
"""


import math, json, os
from settings import *
from typing import Sequence
import mediapipe as mp


pose = mp.solutions.pose.Pose( # type: ignore
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


def check_frame(frame, sample_id: int) -> float:
    """
    Checks is the pose on the frame or not
    
    :param frame: Frame in RGB
    :param sample_id: Sample pose id
    :return: Match percentage (from 0 to 1)
    """
    frame.flags.writeable = False
    results = pose.process(frame)
    frame.flags.writeable = True
    if results is not None and results.pose_landmarks is not None and results.pose_landmarks.landmark is not None:
        return check_id([(landmark.x, landmark.y) for landmark in results.pose_landmarks.landmark], sample_id)
    return 0


def check_id(pose: Sequence, sample_id: int) -> float:
    sample = json.load(open(os.path.sep.join((SAMPLES_PATH, f"{sample_id:02d}.json")), encoding="utf-8"))
    return check_sample(pose, sample)


def check_sample(pose: Sequence, sample: Sequence) -> float:
    conns = [math.atan2(pose[p1][1] - pose[p2][1], pose[p1][0] - pose[p2][0]) for p1, p2 in ((16, 14), (14, 12), (11, 13), (13, 15), 
                                                                                             (28, 26), (26, 24), (23, 25), (25, 27))]
    cost = 0
    for a, b in zip(conns, sample):
        a %= 2 * math.pi
        b %= 2 * math.pi
        cost += (math.pi - abs(abs(a - b) - math.pi)) ** 2
    return math.exp(-cost * 5e-2)