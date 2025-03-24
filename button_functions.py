import game_functions as gf
from file_dialogue import open_file_dialogue, load_json_file
import json
import pygame

def play_button_click(settings):
    """Sets active to true, so board begins iterating"""
    print('begin')
    settings.active = True


def stop_button_click(settings):
    """Sets active to false, board stops iterating"""
    print('stop')
    settings.active = False


def reset_button_click(settings, tiles):
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


def clear_button_click(settings, tiles):
    """Clears the board and wipes history"""
    print('clear')
    if settings.active == False:
        # reset the frame and highest frame to 0
        settings.frame, settings.highest_frame = 0, 0
        for tile in tiles:
            tile.colour = settings.dead_col
        settings.frame_tile_config_dict = {}


def forward_button_click(settings, tiles):
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
            gf.check_neighbours(tiles, settings)      
            gf.evaluate_neighbours(tiles, settings)
            #change state of appropriate tiles
            gf.iterate_tiles(tiles, settings)
            # iterate the frame by 1
            settings.frame += 1
            print('current frame = ', settings.frame)
            print('highest frame = ', settings.highest_frame)

def back_button_click(settings, tiles):
    """Moves the board back one iteration, loded from the settings.frame_tile_config dictionary"""
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

def import_button_click(settings, tiles):
    """Import a custom board cofiguration from an external source"""
    file_path = open_file_dialogue()
    # If a file was selected, load it
    if file_path:
        json_data = load_json_file(file_path)
        file_selected = True
        #print("Loaded JSON data:", json_data)
    else:
        file_selected = False
        print("No file selected")
    if file_selected:
        for tile in tiles:
            for tile_name, config in json_data.items():
                if tile.name == tile_name:
                    if config == 0:
                        tile.colour = settings.dead_col
                    elif config == 1:
                        tile.colour = settings.live_col

def export_button_click(settings):
    """Change state of game to 'exporting"""
    print("Export button clicked")
    settings.exporting = True

def cancel_button_click(settings):
    """Change state of game out of 'exporting"""
    settings.exporting = False
    settings.user_typing = False

def save_button_click(settings):
    """Saves the tile configuration to a local file name defined by settings.user_text, and changes the 'settings.user_typing' attribute to false"""
    json_export_data = settings.frame_tile_config_dict[settings.frame]
    filepath = "D:\python_learning\personalProjects\PythonProjects\game_of_life/files/" + settings.user_text + ".json"
    with open(filepath, 'w') as json_file:
        json.dump(json_export_data, json_file)
    settings.exporting = False
    settings.user_typing = False

def text_button_click(settings):
    """Changes state of game to 'user typing', where user keystrokes are logged to create filename for export"""
    settings.user_typing = True

def add_text(event, settings):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            settings.user_text = settings.user_text[:-1]
        else:
            settings.user_text += event.unicode