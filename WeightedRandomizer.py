import random


# Heavily based on Hyperboreus's answer at https://stackoverflow.com/a/14993631

class WeightedRandomizer:
    def __init__(self, weights):
        self.__max = .0
        self.__weights = []
        for value, weight in weights.items():
            self.__max += weight
            self.__weights.append((self.__max, value))

    def random(self):
        r = random.random() * self.__max
        for ceil, value in self.__weights:
            if ceil > r:
                return value
