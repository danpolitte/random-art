import random
from WeightedRandomizer import WeightedRandomizer


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

    def __str__(self):
        return '(\n\tR: {}\n\tG: {}\n\tB: {}\n)'.format(str(self.args[0]), str(self.args[1]), str(self.args[2]))
        #return '(' + str(self.args[0]) + ', ' + str(self.args[1]) + ', ' + str(self.args[2]) + ')'


c_expr_randomizer = WeightedRandomizer({
    'A': 2,
    'neg': 2,
    'cond': 1,
    'add': 3,
    'mult': 3
})


class CExpression:
    def __init__(self, d_rem):
        # At maximum depth, default to simplest option
        if d_rem <= 0:
            self.type = 'A'
        else:
            self.type = c_expr_randomizer.random()

        # Additional decrementing of the depth to keep the tree trimmed
        while d_rem <= 0 and random.random() > 0.5:
            d_rem -= 1

        if self.type == 'A':
            self.args = [AExpression(d_rem-1)]
        elif self.type == 'neg':
            self.args = [CExpression(d_rem - 1)]
        elif self.type == 'cond':
            self.args = [CExpression(d_rem-1), CExpression(d_rem-1), CExpression(d_rem-1)]
        elif self.type == 'add':
            self.args = [CExpression(d_rem-1), CExpression(d_rem-1)]
        elif self.type == 'mult':
            self.args = [CExpression(d_rem-1), CExpression(d_rem-1)]

    def evaluate(self, x, y):
        # First, evaluate all subexpressions
        arg_evals = [expr.evaluate(x, y) for expr in self.args]
        if self.type == 'A':
            return arg_evals[0]
        elif self.type == 'neg':
            return -arg_evals[0]
        elif self.type == 'cond':
            return arg_evals[1] if arg_evals[0] > 0 else arg_evals[2]
        elif self.type == 'add':
            # Division by 2 to map to [-1, 1]
            return (arg_evals[0] + arg_evals[1]) / 2
        elif self.type == 'mult':
            return arg_evals[0] * arg_evals[1]

    def __str__(self):
        if self.type == 'A':
            return str(self.args[0])
        elif self.type == 'neg':
            return '-(' + str(self.args[0]) + ')'
        elif self.type == 'cond':
            return '(if ' + str(self.args[0]) + '>0 then ' + str(self.args[1]) + ' else ' + str(self.args[1]) + ')'
        elif self.type == 'add':
            return 'add(' + str(self.args[0]) + ', ' + str(self.args[1]) + ')'
        elif self.type == 'mult':
            return 'mult(' + str(self.args[0]) + ', ' + str(self.args[1]) + ')'


a_expr_randomizer = WeightedRandomizer({
    'num': 1,
    'x': 1,
    'y': 1
})


class AExpression:
    def __init__(self, d_rem):
        # At maximum depth, default to simplest option
        # TODO: wait, does this distinction make sense for this level?
        if d_rem <= 0:
            self.type = 'num'
        else:
            self.type = a_expr_randomizer.random()

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

    def __str__(self):
        if self.type == 'num':
            return '{:.3}'.format(self.value)
        elif self.type == 'x':
            return 'x'
        elif self.type == 'y':
            return 'y'
