#!/usr/bin/env python3

from __future__ import annotations
import random

'''
module maze:
    Provides classes for generating and parsing a maze
'''

class Cell:
    def __init__(self, val: str, x: int, y: int):
        self.visited = False
        self.val = val
        self.x = x
        self.y = y
    
    def __str__(self):
        return self.val

    def __repr__(self):
        return f"Cell('{self.val}', {self.x}, {self.y})"

    def near(self, other: Cell) -> bool:
        if self.x is other.x:
            return abs(self.y - other.y) is 2
        elif self.y is other.y:
            return abs(self.x - other.x) is 2
        return False

class Maze:
    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.cols = [ [ Cell("+", x, y) for y in range(h) ] for x in range(w) ]
        self.visited_count = 0
    
    def __str__(self) -> str:
        return "\n".join([
            ",".join([ str(self.cols[x][y]) for x in range(self.w) ])
            for y in range(self.h) ])

    def __getitem__(self, key: int) -> List[Cell]:
        return self.cols[key]

    def cells(self) -> List[Cell]:
        return [ self.cols[x][y] for y in range(self.h) for x in range(self.w) ]

    def in_bounds(self, x: int, y: int, dist: int = 1) -> bool:
        return x > 0 and x < self.w - dist and y > 0 and y < self.h - dist

    def neighbors(self, cell: Cell, dist: int = 2) -> List[Cell]:
        return [ self.cols[x][y] for x, y in [ 
            (cell.x, cell.y - dist), (cell.x, cell.y + dist),
            (cell.x - dist, cell.y), (cell.x + dist, cell.y)
            ] if self.in_bounds(x, y, dist - 1) ]

    def between(self, cell: Cell, other: Cell) -> Cell:
        return self.cols[cell.x + (other.x - cell.x) // 2][cell.y + (other.y - cell.y) // 2]

class RandomMaze(Maze):
    '''
    Maze generation is handled via a randomized backtracking algorithm
    '''
    def __init__(self, w: int, h: int, bypass: bool = True):
        super().__init__(w, h)
        sx, sy = 0, random.randint(2, h - 2)
        current = self.cols[sx][sy]
        current.val = "S"
        current.visited = True
        stack = []
        short = self.visited_count < self.w * self.h
        while (bypass and short) or len([ c for c in self.cells() if not c.visited ]) > 0:
            unvisited_neighbors = [ c for c in self.neighbors(current) if not c.visited ]
            if len(unvisited_neighbors) > 0:
                stack.append(current)
                lucky = random.choice(unvisited_neighbors)
                wall = self.between(current, lucky)
                wall.val = lucky.val = " "
                wall.visited = lucky.visited = True
                current = lucky
            elif len(stack) > 0:
                current = stack.pop()
            else:
                break

        potentials = [ cell for cell in self.cols[w - 2]
                if len([ n for n in self.neighbors(cell, 1) if n.val is " " ]) > 0 ]
        exit = random.choice(potentials)
        exit.val = " "
        self.cols[exit.x + 1][exit.y].val = "E"
        for c in self.cells():
            c.visited = False

class CsvMaze(Maze):
    def __init__(self, csv: str):
        s = [ line.rstrip('\n').split(',') for line in csv.splitlines() ]
        self.w, self.h = len(s[0]), len(s)
        super().__init__(self.w, self.h)
        self.cols = []
        for x in range(self.w):
            self.cols.append([])
            for y in range(self.h):
                self.cols[x].append(Cell(s[y][x], x, y))

class FileMaze(CsvMaze):
    def __init__(self, filepath: str):
        super().__init__("".join(open(filepath).readlines()))

if __name__ == "__main__":
    filepath = "example.csv"
    print(RandomMaze(81, 41), file=open(filepath, "w"))
    m = FileMaze(filepath)
    print(m)
