import pygame
import numpy as np
import random
from .meteor import Meteor
from .controller import Controller
from .brain import Brain

E = pygame.Vector2(1, 0)
NE = pygame.Vector2(0.707, -0.707)
N = pygame.Vector2(0, -1)
NW = pygame.Vector2(-0.707, -0.707)
W = pygame.Vector2(-1, -0)
SW = pygame.Vector2(-0.707, 0.707)
S = pygame.Vector2(0, 1)
SE = pygame.Vector2(0.707, 0.707)

class Player:
    
    def __init__(self, pos, weights):
        self.position = pos
        self.lifetime = 0
        self.isAlive = True
        self.color = "green"
        self.controller = Controller()
        self.speed = 400
        self.screen = pygame.display.get_surface()
        self.weights = weights
        self.brain = Brain(weights)
        self.sensors = [E, NE, N, NW, W, SW, S, SE]
        self.perception = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def update(self, dt, keys):
        if (self.position.x > 1160 or self.position.x < 120): self.isAlive = False
        if (self.position.y > 600 or self.position.y < 120): self.isAlive = False

        if self.isAlive: 
            self.lifetime += dt
            self.move(dt)
        else:
            self.color = "red"

        pygame.draw.circle(self.screen, self.color, self.position, 20)

    # For each direction, get the weight of closer meteor
    def sense(self, meteor_set: list[Meteor]):
        # Setting negative perception as base allows empty spaces to have some weight
        perception = np.array([-.1, -.1, -.1, -.1, -.1, -.1, -.1, -.1, 0, 0])

        for meteor in meteor_set:
            idx = 0
            for sensor in self.sensors:
                delta = meteor.pos - self.position

                # Kill the player if meteor is too close
                if delta.magnitude() < 60.0: self.isAlive = False

                proj = pygame.Vector2.dot(sensor, delta)
                # Check the closest sensor to the meteor cos(22.5deg) ~ 0.9239
                sensation = 61.0/(proj+1) if 150 > proj > 0.9238*delta.magnitude() else -.1
                perception[idx] = np.max([sensation, perception[idx]]) 
                idx += 1

            # Last two sensors to the borders
            perception[8] = ((self.position.x - 640)/540)**3
            perception[9] = ((self.position.y - 360)/260)**3
        self.perception = perception

    def get_new_pos(self, keys, dt):
        x,y = self.controller.get_keys(keys)
        self.position.y += y * 300 * dt
        self.position.x += x * 300 * dt
    
    def move(self, dt):
        x,y = self.brain.thought(self.perception)
        self.position.y += y * self.speed * dt
        self.position.x += x * self.speed * dt


        