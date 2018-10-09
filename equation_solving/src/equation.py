#!/usr/bin/env python3

from operator import add, sub, mul, mod, floordiv as div
from random import choice, randrange
from itertools import product

ops = {
    add: "+",
    sub: "-",
    mul: "*",
    div: "/",
    mod: "%"
}

class Expression:
    def __init__(self, op, x, y):
        self.x = x
        self.y = y
        self.op = op
        self.value = None
    
    def __repr__(self):
        return f"({self.x} {ops[self.op]} {self.y})"

    def __int__(self):
        return self.op(int(self.x), int(self.y))

    def level(self):
        l = self.x.level() if isinstance(self.x, Expression) else 1
        r = self.y.level() if isinstance(self.y, Expression) else 1
        assert l == r # ensure tree is balanced
        return 1 + l

    def fromstring(exp):
        mid = len(exp) // 2
        if mid is 0:
            return int(exp)
        op = [ k for k, v in ops.items() if v == exp[mid] ][0]
        left = Expression.fromstring(exp[1:mid-1])
        right = Expression.fromstring(exp[mid+2:-1])
        return Expression(op, left, right)

def exp_tree(depth):
    op = choice(list(ops.keys()))

    if depth is 0:
        return randrange(10)

    a, b = exp_tree(depth - 1), exp_tree(depth - 1)
    while (op is mod or op is div) and int(b) is 0:
        b = exp_tree(depth - 1)

    return Expression(op, a, b)

def challenge():
    e = 0
    while int(e) == 0:
        e = exp_tree(4)

    s = str(e)
    for op in ops.values():
        s = s.replace(op, "?")

    return f"{s} => {int(e)}"

def solve(chall):
    s, _, goal = chall.partition(" => ")
    comb = product(ops.values(), repeat=s.count("?"))
    for guess in comb:
        i = iter(guess)
        attempt = "".join([ c if c is not "?" else next(i) for c in s ])
        e = Expression.fromstring(attempt)
        try: 
            if int(e) == int(goal):
                break
        except ZeroDivisionError:
            pass
    return e

if __name__ == "__main__":
    chal = challenge()
    print(chal)
    sol = solve(chal)
    print(sol)
