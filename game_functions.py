import pygame
from tile import Tile
import sys 

def create_board(settings, screen, tiles):

    """find the dimensions of tiles in the board"""
    for col_num in range(settings.cols):
        print("Col num", col_num)
        for row_num in range(settings.rows):
            print("Row num", row_num)
            tile = Tile(settings ,screen)
            tile.rect.left = (col_num * tile.width)
            tile.rect.top = (row_num * tile.height)
            tile.col = col_num
            tile.row = row_num
            tile.name = str(col_num) + ' : ' + str(row_num)
            tiles.add(tile)

def draw_screen(tiles, buttons, frame_counter, settings):
    """draw all elements on the screen"""
    for tile in tiles:
        tile.draw_tile()
    for button in buttons:
        button.draw_button()
    frame_counter.prep_msg('Frame: ' + str(settings.frame))
    frame_counter.draw_counter()
    



def check_events(settings, tiles, play_button, reset_button, stop_button, forward_button, back_button, clear_button):
    """check user input"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if settings.active == False:
                check_rect(settings, tiles, mouse_x, mouse_y)   
            check_button(settings, play_button, reset_button, stop_button, mouse_x, mouse_y, tiles, forward_button, back_button, clear_button)

def check_rect(settings, tiles, mouse_x, mouse_y):
    """change the state of a tile based on user input"""
    for tile in tiles:
        if tile.rect.collidepoint(mouse_x, mouse_y):
            tile.change_state(settings)


def check_neighbours(tiles, settings):
    """locate all the neighbours of the tile and add up the amount of dead neighbours and alive ones"""
    for tile in tiles:
        #set dead/live neighbours as zero
        dead_neighbours = 0
        live_neighbours = 0
        for n_tile in tiles:
            #find neighbours on the row below
            if n_tile.row == tile.row + 1:
                if n_tile.col == tile.col or n_tile.col == tile.col + 1 or n_tile.col == tile.col - 1:
                    if n_tile.colour == settings.dead_col:
                        dead_neighbours += 1
                    elif n_tile.colour == settings.live_col:
                        live_neighbours += 1
            #find neighbours on the same row    
            elif n_tile.row == tile.row:
                if n_tile.col == tile.col + 1 or n_tile.col == tile.col - 1:                
                    if n_tile.colour == settings.dead_col:
                        dead_neighbours += 1
                    elif n_tile.colour == settings.live_col:
                        live_neighbours += 1 
            #find neighbours on the row above
            elif n_tile.row == tile.row - 1:
                if n_tile.col == tile.col or n_tile.col == tile.col + 1 or n_tile.col == tile.col - 1:                   
                    if n_tile.colour == settings.dead_col:
                        dead_neighbours += 1
                    elif n_tile.colour == settings.live_col:
                        live_neighbours += 1  


        # check if sum of neighbours < 8, then add the differrence to deal neighbours
        # add the dead/live neighbours as attiributes for the tile
        total_neighbours = live_neighbours + dead_neighbours
        if total_neighbours < 8:
            difference = 8 - total_neighbours
            dead_neighbours += difference
        
        # assign the live/dead neighbours values to the tiles attributes
        tile.live_neighbours = live_neighbours
        tile.dead_neighbours = dead_neighbours


        



def evaluate_neighbours(tiles, settings):
    """determine whether the tile will change state on the next iteration based on the amount of dead/live neighbours"""
    for tile in tiles:
        if tile.colour == settings.live_col:
            if tile.live_neighbours < 2:
                tile.change_next_turn = True
            if tile.live_neighbours > 3:
                tile.change_next_turn = True
        if tile.colour == settings.dead_col:
            if tile.live_neighbours == 3:
                tile.change_next_turn = True
        

def check_button(settings, play_button, reset_button, stop_button, mouse_x, mouse_y, tiles, forward_button, back_button, clear_button):
    """process user input on the buttons"""

    if play_button.rect.collidepoint(mouse_x, mouse_y):
        """Sets active to true, so board begins iterating"""
        print('begin')
        settings.active = True

    elif stop_button.rect.collidepoint(mouse_x, mouse_y):
        """Sets active to false, board stops iterating"""
        print('stop')
        settings.active = False
        
    elif reset_button.rect.collidepoint(mouse_x, mouse_y):
        """Reset only works when board is not iterating. It sets the board back to the state at frame 0, and clears the settings.frame_tile_config dict."""
        print('reset')
        if settings.active == False:
            # reset the frame and highest frame to 0
            settings.frame, settings.highest_frame = 0, 0
            # reset the board to state at frame = 0
            for tile in tiles:
                for tile_name, config in settings.frame_tile_config_dict[settings.frame].items():
                    if tile.name == tile_name:
                        if config == 0:
                            tile.colour = settings.dead_col
                        elif config == 1:
                            tile.colour = settings.live_col

            settings.frame_tile_config_dict = {}

    elif clear_button.rect.collidepoint(mouse_x, mouse_y):
        """Clears the board and wipes history"""
        print('clear')
        if settings.active == False:
            # reset the frame and highest frame to 0
            settings.frame, settings.highest_frame = 0, 0
            for tile in tiles:
                tile.colour = settings.dead_col
            settings.frame_tile_config_dict = {}
    
    elif forward_button.rect.collidepoint(mouse_x, mouse_y):
        """Moves board forward one iteration, different methods depending on if frame + 1 has already been renderes (meaning it has an entry in settings.frame_tile_config dictionary)"""
        print('forward')
        if settings.active == False:
            # This if statement checks if the board config we are requesting has already been calculated, and retreieves in from the dictionary. This avoids unnesseccary computation
            if (settings.frame + 1) <= settings.highest_frame:
                print("rerendering frame previously calcuated")
                settings.frame += 1
                print('current frame = ', settings.frame)
                print('highest frame = ', settings.highest_frame)
                # This block of code 
                for tile in tiles:
                    for tile_name, config in settings.frame_tile_config_dict[settings.frame].items():
                        if tile.name == tile_name:
                            if config == 0:
                                tile.colour = settings.dead_col
                            elif config == 1:
                                tile.colour = settings.live_col

            else:
                print("new frame being rendered")
                check_neighbours(tiles, settings)      
                evaluate_neighbours(tiles, settings)
                #change state of appropriate tiles
                iterate_tiles(tiles, settings)
                # iterate the frame by 1
                settings.frame += 1
                print('current frame = ', settings.frame)
                print('highest frame = ', settings.highest_frame)

    elif back_button.rect.collidepoint(mouse_x, mouse_y):
        print('back')
        if settings.active == False:
            if settings.frame -1 > -1:
                settings.frame -= 1
                print('current frame = ', settings.frame)
                print('highest frame = ', settings.highest_frame)
                for tile in tiles:
                    for tile_name, config in settings.frame_tile_config_dict[settings.frame].items():
                        if tile.name == tile_name:
                            if config == 0:
                                tile.colour = settings.dead_col
                            elif config == 1:
                                tile.colour = settings.live_col

        else:
            pass




def iterate_tiles(tiles, settings):
    for tile in tiles:
        if tile.change_next_turn == True:
            tile.change_state(settings)

def save_board(tiles, settings):
    """Save the configuration of the tiles dead/live attributes for redisplaying when reset button pressed"""
    tile_format = {}
    for tile in tiles:
        if tile.colour == settings.dead_col:
            tile_format[tile.name] = 0
        elif tile.colour == settings.live_col:
            tile_format[tile.name] = 1
    settings.frame_tile_config_dict[settings.frame] = tile_format
    #print('saved format from frame ' + str(settings.frame))

