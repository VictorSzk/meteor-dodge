import pygame
import numpy as np
import random
from .meteor import Meteor

class MeteorSpawner:

    def __init__(self, clock):
        self.clock = clock
        self.timer = 0
        self.meteor_set: list[Meteor] = []
    
    def update(self, playerposition, dt):
        if (self.timer > 2):
            rand_array = [random.randint(0,1), random.uniform(0,1)] 
            r_idx = random.randint(0,1)
            random_pos = pygame.Vector2(50 + 1180*rand_array[r_idx], 50 + 620*rand_array[(r_idx + 1) % 2])
            self.meteor_set.append(Meteor(self.clock, random_pos, playerposition))
            self.timer = 0

        if len(self.meteor_set) > 20:
            self.meteor_set.pop(0)

        for x in self.meteor_set:
            x.update()

        self.timer += dt

