from settings import Settings
import pygame
import game_functions as gf
from pygame.sprite import Group
import sys
from button import Button
from time import sleep
from frame_counter import FrameCounter

def run_game():
    #intiialise pygame
    pygame.init()

    #initiaise settings and tiles
    settings = Settings()
    tiles = Group()

    #create the window
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    screen.fill(settings.bg_colour)
    pygame.display.set_caption("Game of Life")  

    #create the buttons
    buttons = []
    play_button = Button(settings, screen, 'Begin', 0, settings.button_top1, settings.button_width1)
    reset_button = Button(settings, screen, 'Reset', 2*settings.screen_width/3, settings.button_top1, settings.button_width1)
    stop_button = Button(settings, screen, 'Stop', settings.screen_width/3, settings.button_top1, settings.button_width2)
    forward_button = Button(settings, screen, 'Forward', 2 *settings.screen_width/3, settings.button_top2, settings.button_width1)
    back_button = Button(settings, screen, 'Back', 0, settings.button_top2, settings.button_width1)
    import_button =Button(settings, screen, 'Import', settings.screen_width/3, settings.button_top2, settings.button_width2)
    export_button = Button(settings, screen, 'Export', settings.screen_width/2, settings.button_top2, settings.button_width2)
    clear_button = Button(settings, screen, 'Clear', settings.screen_width/2, settings.button_top1, settings.button_width2)
    buttons.extend([play_button, reset_button, stop_button, forward_button, back_button, import_button, export_button, clear_button])

    #create the board of tiles
    gf.create_board(settings, screen, tiles)

    #create a frame counter
    frame_counter = FrameCounter(settings, screen, str(settings.frame))

    
    #start the game loop
    while True:

        # actions which happen every loop independent if board is iterating
        gf.draw_screen(tiles, buttons, frame_counter, settings) # draw all elements of the game
        gf.save_board(tiles, settings,) #
        gf.check_events(settings, tiles, play_button, reset_button, stop_button, forward_button, back_button, clear_button)
        

        if settings.frame >= settings.highest_frame:
            settings.highest_frame = settings.frame

        # actions which happen when board is playing
        if settings.active == True:
            #evaluate if tile needs to change state
            gf.check_neighbours(tiles, settings)      
            gf.evaluate_neighbours(tiles, settings)

            #change state of appropriate tiles
            gf.iterate_tiles(tiles, settings)
            
            #pause until next iteration
            sleep(settings.sleep_timer)

            # iterate the frame by 1
            settings.frame += 1
            # set highest frame parameter

            print('current frame = ', settings.frame)
            #print('highest frame = ', settings.highest_frame)

        #display most recent screen
        pygame.display.flip()

run_game()