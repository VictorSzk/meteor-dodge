import pygame

class Meteor:
    def __init__(self, clock, initialpos: pygame.Vector2, playerpos: pygame.Vector2):
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.pos = initialpos
        self.direction = (playerpos - initialpos).normalize()
        self.clock = clock
        self.dt = self.clock.tick(60)/1000
        self.speed = 50

    def update(self):
        self.calcnewpos()
        pygame.draw.circle(self.screen, "black", self.pos, 40)

    def calcnewpos(self):
        self.pos.x += self.direction.x * self.speed * self.dt
        self.pos.y += self.direction.y * self.speed * self.dt