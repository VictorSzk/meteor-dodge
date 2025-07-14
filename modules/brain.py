import numpy as np

class Brain:
    def __init__(self, weights):
        self.weights = weights

    def thought(self, inputs):
        X = np.dot(inputs, self.weights.x)
        Y = np.dot(inputs, self.weights.y)
        return X,Y

