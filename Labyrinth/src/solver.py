#!/usr/bin/env python3

from __future__ import annotations
from typing import Optional
from maze import Maze, RandomMaze, Cell
import os
import time

'''
module solver:
    Simple demonstration of a maze solving algorithm
    using iterative depth-first search
'''

def solve(m: Maze) -> List[Cell]:
    start = [ c for c in m.cells() if c.val is "S" ][0]
    stack = [ start ]

    cell = stack.pop()
    while cell.val is not "E":
        cell.visited = True
        neighbors = [ c for c in m.neighbors(cell, 1) 
                if c.val is not "+" and not c.visited ]

        if len(neighbors) > 0:
            stack.append(cell)
            stack.append(neighbors[0])

        cell = stack.pop()
    
    return stack

# return the path to solve a maze
def get_path(m: Maze) -> str:
    stack, res = solve(m), ""
    for i in range(1, len(stack)):
        if stack[i].x > stack[i - 1].x:
            direction = "RIGHT"
        elif stack[i].x < stack[i - 1].x:
            direction = "LEFT"
        elif stack[i].y < stack[i - 1].y:
            direction = "UP"
        else:
            direction = "DOWN"
        res += f"{direction},"
    return res + "RIGHT"

# returns the end cell after following a path or None if the path is invalid
def follow_path(m: Maze, path: str) -> Optional[Cell]:
    current = [ c for c in m.cells() if c.val is "S" ][0]
    for direction in path.split(','):
        if direction == "RIGHT":
            x, y = current.x + 1, current.y
        elif direction == "LEFT":
            x, y = current.x - 1, current.y
        elif direction == "UP":
            x, y = current.x, current.y - 1
        elif direction == "DOWN":
            x, y = current.x, current.y + 1
        else:
            return None
        
        if current.val == "+" or not m.in_bounds(x, y, 0):
            return None

        current = m.cols[x][y]

    return current

if __name__ == "__main__":
    m = RandomMaze(89, 53)
    end = follow_path(m, get_path(m))
    assert end is not None and end.val == "E"

    m = RandomMaze(89, 53)
    stack = solve(m)

    for cell in stack:
        os.system('clear')
        m.cols[cell.x][cell.y].val = "-"
        print(m)
        time.sleep(0.01)
