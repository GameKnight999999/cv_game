import math, json, os
from settings import *


def check_id(pose, sample_id) -> float:
    sample = json.load(open(os.path.sep.join((SAMPLES_PATH, f"{sample_id:02d}.json")), encoding="utf-8"))
    return check_sample(pose, sample)


def check_sample(pose, sample) -> float:
    conns = [math.atan2(pose[p1][1] - pose[p2][1], pose[p1][0] - pose[p2][0]) for p1, p2 in ((16, 14), (14, 12), (11, 13), (13, 15), 
                                                                                             (28, 26), (26, 24), (23, 25), (25, 27))]
    cost = 0
    for a, b in zip(conns, sample):
        a %= 2 * math.pi
        b %= 2 * math.pi
        cost += (math.pi - abs(abs(a - b) - math.pi)) ** 2
    return math.exp(-cost * 0.3)