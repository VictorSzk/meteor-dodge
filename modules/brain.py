import numpy as np
import math

class Weights:
    def __init__(self, weights_x, weights_y):
        self.x = weights_x
        self.y = weights_y

class Brain:
    def __init__(self, weights):
        self.weights = weights
        self.movements = lambda x: (1-math.exp(-x))/(1+math.exp(-x))

    def thought(self, inputs):
        X = np.dot(inputs, self.weights.x)
        Y = np.dot(inputs, self.weights.y)

        return self.movements(X),self.movements(Y)

