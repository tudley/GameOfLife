import pygame
from pygame.sprite import Sprite



class Tile(Sprite):
    """A class modelling a tile"""
    def __init__(self, settings, screen, name=None, live_neigbours = 0, dead_neigbours = 0, colour = (0, 0, 0)):
        super(Tile, self).__init__()
        self.width = settings.tile_width
        self.height = settings.tile_height
        self.perimiter = settings.tile_perimiter
        self.rect = pygame.Rect(0, 0, settings.tile_width, settings.tile_height)
        self.colour = colour
        self.screen = screen
        self.change_next_turn = False
        self.name = None
        self.live_neighbours = live_neigbours
        self.dead_neighbours = dead_neigbours

    def draw_tile(self):
        """Draw a tile onto the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)

    def change_state(self, settings):
        """A function to change the alive/dead state of a tile"""
        if self.colour == settings.dead_col:
            self.colour = settings.live_col
        elif self.colour == settings.live_col:
            self.colour = settings.dead_col
        self.change_next_turn = False