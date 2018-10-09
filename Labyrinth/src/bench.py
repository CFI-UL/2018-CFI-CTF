#!/usr/bin/env python3

from maze import RandomMaze
import time

def timing(f, *args):
    time1 = time.time()
    ret = f(*args)
    time2 = time.time()
    print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

if __name__ == "__main__":
    for i in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        timing(RandomMaze, i, i)
        timing(RandomMaze, i, i, False)
