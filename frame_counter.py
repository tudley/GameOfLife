import pygame
import pygame.font

class FrameCounter():
    """A class to model a box which displays to the user the frame the board is currently on"""
    def __init__(self, settings, screen, msg):

        self.screen = screen
        self.bg_colour = settings.frame_counter_colour
        self.text_colour = settings.live_col

        self.rect = pygame.Rect(settings.frame_counter_left, settings.frame_counter_top, settings.frame_counter_width, settings.frame_counter_height)  
        self.font = pygame.font.SysFont(None, 48)
        self.prep_msg('Frame: ' + msg)


    def prep_msg(self, msg):
        """Turn a msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_colour, self.bg_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_counter(self):
        """draw blank button and then draw message"""
        self.screen.fill(self.bg_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)