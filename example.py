# Example file showing a circle moving on screen
import pygame
import numpy as np
from modules.player import Player
from modules.meteor_spawn import MeteorSpawner


# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
timer = 0
# meteor_list: list[Meteor] = []

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

player = Player(player_pos)

font = pygame.font.Font('freesansbold.ttf', 12)

meteor_spawner = MeteorSpawner(clock)

# create a text surface object,
# on which text is drawn on it.
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

weights = [{'x': np.array([0]*8), 'y': np.array([0]*8)}] * 8

"""
This game is a simples meteor dodge, control the red circle to avoid rogue 
black circles that can destroy the player on touch
"""

class Game:
    def __init__(self):
        self.timer: float = 0
        self.generation: int = 0
        # self.players: list[Player] = []

    def startGame(self, weights):
        self.timer = 0

    def update(self):

        # Motion area for player
        pygame.draw.rect(screen, "cyan", pygame.Rect(100,100,1080, 520))

        text = font.render(f'lifetime: {player.lifetime}', True, green, blue)
        textRect = text.get_rect()
        textRect.topleft = (0, 0)
        
        screen.blit(text, textRect)


        timer += dt

        keys = pygame.key.get_pressed()
        player.update(dt, keys)


        # Spawn random circle

        meteor_spawner.update(player.position, dt)

        # Check collision with player

        for x in meteor_spawner.meteor_set:
            dist = (x.pos - player.position).magnitude_squared()
            if dist < 3600:
                player.isAlive = False
                pass

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # Motion area for player
    pygame.draw.rect(screen, "cyan", pygame.Rect(100,100,1080, 520))

    text = font.render(f"lifetime: {player.lifetime}",True, green, blue)
    textRect = text.get_rect()
    textRect.topleft = (0, 0)
    screen.blit(text, textRect)

    text = font.render(f"sensors: {player.perception}",True, green, blue)
    textRect = text.get_rect()
    textRect.topleft = (0, 20)
    screen.blit(text, textRect)


    timer += dt

    keys = pygame.key.get_pressed()
    player.update(dt, keys)


    # Spawn random circle

    meteor_spawner.update(player.position, dt)

    player.sense(meteor_spawner.meteor_set)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()