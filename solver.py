import sys
from copy import deepcopy

def read_input(filename):
    with open(filename) as f:
        lines = [l.strip() for l in f if l.strip()]
    h, n, k = map(int, lines[0].split())
    tubes = []
    for i in range(1, n + 1):
        row = list(map(int, lines[i].split()))
        tubes.append(row)
    # Add empty tubes
    for _ in range(k):
        tubes.append([])
    return h, n, k, tubes

def is_goal(tubes, h):
    for tube in tubes:
        if len(tube) == 0:
            continue
        if len(tube) != h:
            return False
        if len(set(tube)) != 1:
            return False
    return True