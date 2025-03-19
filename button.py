import pygame
import pygame.font


class Button():
    """A class modelling a button"""
    def __init__(self, settings, screen, msg, left, top, width):
        self.screen = screen
        self.button_colour = (0, 0, 0)
        self.text_colour = (255, 255, 255)
        self.button_height = settings.button_height
        self.button_width = width
        self.button_top = top
        self.button_left = left
        self.font = pygame.font.SysFont(None, 48)

        #build the buttons rect and center it
        self.rect = pygame.Rect(self.button_left, self.button_top, self.button_width, self.button_height)
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn a msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """draw blank button and then draw message"""
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
