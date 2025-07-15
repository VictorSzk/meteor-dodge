# Example file showing a circle moving on screen
import pygame
import numpy as np
import random
import math
from modules.player import Player
from modules.meteor_spawn import MeteorSpawner
from modules.brain import Weights

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
timer = 0
# meteor_list: list[Meteor] = []

PLAYER_POS = pygame.Vector2(640, 360)

def random_weight():
    return Weights([random.uniform(-2,2) for _ in range(10)], [random.uniform(-2,2) for _ in range(10)])

def random_new_weight(weight: Weights, growth: float):

    bias = np.array([0,0,0,0,0,0,0,0,-0.1,-0.1])
    new_x = np.add(weight.x, [random.gauss(0,growth) for _ in range(10)])
    new_y = np.add(weight.y, [random.gauss(0,growth) for _ in range(10)])
    return Weights(new_x, new_y)


font = pygame.font.Font('freesansbold.ttf', 12)

meteor_spawner = MeteorSpawner(clock)

# create a text surface object,
# on which text is drawn on it.
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

"""
This game is a simples meteor dodge, control the red circle to avoid rogue 
black circles that can destroy the player on touch
"""

class Game:
    def __init__(self, population):
        self.timer: float = 0
        self.generation: int = 1
        self.population = population
        self.players: list[Player] = [Player(PLAYER_POS.copy(), random_weight()) for _ in range(population)]

    def startGame(self):
        self.timer = 0
        self.generation += 1
        meteor_spawner.clean()
        self.get_new_generation()

    def update(self, dt):

        screen.fill("purple")

        # Motion area for player
        pygame.draw.rect(screen, "cyan", pygame.Rect(100,100,1080, 520))


        # Spawn random circle


        self.timer += dt

        keys = pygame.key.get_pressed()

        for player in self.players:
            

            player.update(dt, keys)

            player.sense(meteor_spawner.meteor_set)

        meteor_spawner.update(pygame.Vector2(PLAYER_POS), dt)

        idx = 0

        all_alive = False


        text = font.render(f'Generation: {self.generation}', True, green, blue)
        textRect = text.get_rect()
        textRect.topleft = (0, 0)
        screen.blit(text, textRect)

        for player in self.players:
            # Print lifetime of each player
            text = font.render(f'Player {idx+1}: {player.lifetime:.3f}', True, player.color, blue)
            textRect = text.get_rect()
            textRect.topleft = (0, 20*(idx+1))
            screen.blit(text, textRect)
            idx+=1

            all_alive = all_alive or player.isAlive

        if not all_alive: self.startGame()


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    def get_new_generation(self):
        max_idx = 0
        max_lifetime = 0
        for i in range(8):
            if self.players[i].lifetime >= max_lifetime:
                max_lifetime = self.players[i].lifetime
                max_idx = i
            
        mutation = math.floor(max_lifetime/5)
        winner_weight = self.players[max_idx].weights
        self.players.clear()
        self.players = [Player(PLAYER_POS.copy(), winner_weight)] + [Player(PLAYER_POS.copy(), random_new_weight(winner_weight, 0.90**(mutation))) for _ in range(self.population-1)]



game = Game(16)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update(dt)

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("purple")

    # Motion area for player
    # pygame.draw.rect(screen, "cyan", pygame.Rect(100,100,1080, 520))

    
    ## Checking if perception is working as intended
    # idx = 0
    # for direction in ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]:
    #     text = font.render(f"{direction}: {player.perception[idx]:.3f}",True, green, blue)
    #     textRect = text.get_rect()
    #     textRect.topleft = (0, 20*(idx+1))
    #     screen.blit(text, textRect)
    #     idx+=1


    # timer += dt

    # keys = pygame.key.get_pressed()
    # player.update(dt, keys)


    # Spawn random circle

    # meteor_spawner.update(player.position, dt)

    # player.sense(meteor_spawner.meteor_set)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()