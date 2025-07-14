import numpy as np
import pygame

# Get game states and output commanders

class Controller:
    def __init__(self):
        pass

    def get_keys(self, keys):
        X, Y = 0, 0

        if keys[pygame.K_w]:
            Y -= 1
        if keys[pygame.K_s]:
            Y += 1
        if keys[pygame.K_a]:
            X -= 1
        if keys[pygame.K_d]:
            X += 1
        
        return X,Y