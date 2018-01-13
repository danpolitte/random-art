import random


class EExpression:
    def __init__(self, d_rem):
        # Single-choice

        # Additional decrementing of the depth to keep the tree trimmed
        while d_rem <= 0 and random.random() > 0.5:
            d_rem -= 1

        self.args = [CExpression(d_rem-1), CExpression(d_rem-1), CExpression(d_rem-1)]

    def evaluate(self, x, y):
        # First, evaluate all subexpressions
        arg_evals = [expr.evaluate(x, y) for expr in self.args]
        # Just return the ordered triplet
        return arg_evals[0], arg_evals[1], arg_evals[2]


class CExpression:
    def __init__(self, d_rem):
        # At maximum depth, default to simplest option
        if d_rem <= 0:
            self.type = 'A'
        else:
            # Random choice between alternatives
            alts = ['A']*2 + ['add']*3 + ['mult']*3
            self.type = random.choice(alts)

        # Additional decrementing of the depth to keep the tree trimmed
        while d_rem <= 0 and random.random() > 0.5:
            d_rem -= 1

        if self.type == 'A':
            self.args = [AExpression(d_rem-1)]
        elif self.type == 'add':
            self.args = [CExpression(d_rem-1), CExpression(d_rem-1)]
        elif self.type == 'mult':
            self.args = [CExpression(d_rem-1), CExpression(d_rem-1)]

    def evaluate(self, x, y):
        # First, evaluate all subexpressions
        arg_evals = [expr.evaluate(x, y) for expr in self.args]
        if self.type == 'A':
            return arg_evals[0]
        elif self.type == 'add':
            # Division by 2 to map to [-1, 1]
            return (arg_evals[0] + arg_evals[1]) / 2
        elif self.type == 'mult':
            return arg_evals[0] + arg_evals[1]


class AExpression:
    def __init__(self, d_rem):
        # At maximum depth, default to simplest option
        # TODO: wait, does this distinction make sense for this level?
        if d_rem <= 0:
            self.type = 'num'
        else:
            alts = ['num'] + ['x'] + ['y']
            self.type = random.choice(alts)

        # Additional decrementing of the depth to keep the tree trimmed
        while d_rem <= 0 and random.random() > 0.5:
            d_rem -= 1

        if self.type == 'num':
            self.value = random.uniform(-1, 1)

        # x and y require no preparatory work

    def evaluate(self, x, y):
        if self.type == 'num':
            return self.value
        elif self.type == 'x':
            return x
        elif self.type == 'y':
            return y
