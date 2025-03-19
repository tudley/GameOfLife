# Test imports:
import unittest

# Pygame imports:
import pygame
from pygame.sprite import Group

# Self-written file imports:
from tile import Tile
import game_functions as gf
from settings import Settings
#import main


class TestTile(unittest.TestCase):
    """Tests for the class Tile."""

    def setUp(self):
        """Builds all the required objects before each unit test."""
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.tile = Tile(self.settings, self.screen)

    def test_change_state_from_dead_to_live(self):
        """Test the change state works."""
        # tile colour is default to 'dead col'
        self.tile.change_state(self.settings)
        # now tile colour should be 'live col'
        self.assertTrue(self.tile.colour == self.settings.live_col)

    def test_change_state_from_live_to_dead(self):
        """Test the change state works."""
        # tile is default to 'dead col'
        self.tile.change_state(self.settings)
        # now tile colour should be 'live col'
        self.tile.change_state(self.settings)
        # now tile colour should be changed back to 'dead col'
        self.assertTrue(self.tile.colour == self.settings.dead_col)

class TestGameFunctions(unittest.TestCase):
    """Tests all the functions in game_functions."""

    def setUp(self):
        """builds all the required objects for the unit tests."""
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.tile = Tile(self.settings, self.screen)
        self.tiles = Group()
        gf.create_board(self.settings, self.screen, self.tiles)

    def test_gf_create_board(self):
        """"Test the gf.create_board() function creates a board correctly."""
        
        # assert it createds the correct about of tiles, equal to settings.rows * settings.cols
        self.assertTrue(self.tiles.__len__() == self.settings.rows * self.settings.cols)

        # assert each tile has an appropriate name
        string_names = []
        for x in range(self.settings.cols):
            for y in range(self.settings.rows):
                string_name = "tile " + str(y) + " : " + str(x)
                string_names.append(string_name)
        for tile, name in zip(self.tiles, string_names):
            self.assertEqual(tile.name, name)

    def test_gf_check_rect(self):
        """Test the gf.check_rect() function"""
        # note check_rect() is only called when event.type == pygame.MOUSEBUTTONDOWN, so we dont need to checkf ro that

        # extract tile(name = 'tile 0 : 0') as 'tile1' and tile(name = 'tile 0 : 1') as 'tile2'
        for tile in self.tiles:
            if tile.name == "tile 0 : 0":
                tile1 = tile
            elif tile.name == "tile 0 : 1":
                tile2 = tile
 
        # case 1: tile 1 is clicked but not tile 2
        # move mousex, mousey to 1 pixel inside tile1's rect
        mouse_x, mouse_y = tile1.rect.left + 1, tile1.rect.top + 1
        gf.check_rect(self.settings, self.tiles, mouse_x, mouse_y)    
        self.assertTrue(tile1.colour == self.settings.live_col and tile2.colour == self.settings.dead_col)

        # case 2: no tile is clicked, assert statement should remain unchanged
        # move mousex 1 pixel out of tile1's rect
        mouse_x = tile1.rect.left - 1
        gf.check_rect(self.settings, self.tiles, mouse_x, mouse_y)    
        self.assertTrue(tile1.colour == self.settings.live_col and tile2.colour == self.settings.dead_col)

        # case 3: tile 1 is clicked, then tile 2 is clicked. This should change the colours of both tiles in the assert statement
        # move mousex 1 pixel inside tiles1's rect
        mouse_x = tile1.rect.left + 1
        gf.check_rect(self.settings, self.tiles, mouse_x, mouse_y)    
        # move mousex 1 pixel inside tiles2's rect
        mouse_x = tile2.rect.left + 1
        gf.check_rect(self.settings, self.tiles, mouse_x, mouse_y)   
        self.assertTrue(tile1.colour == self.settings.dead_col and tile2.colour == self.settings.live_col)


    def test_gf_check_neighbours(self):
        """Test the functionality of the gf.check_neighbours fcuntion."""
        # test cases:
        # 1. ensure a tile with 8 neighbours works correctly
        #   a) all combinations of dead/live neighbours
        # 2. ensure all edge boundaries work correctly

        tile_1 = self.tile
        tile_1.live_neighbours, tile_1.dead_neighbours = 0, 8

        tile_2 = self.tile
        tile_2.live_neighbours, tile_2.dead_neighbours = 1, 7






        
        pass











    def test_gf_evaluate_neighbours(self):
        """Test all conditions on the gf.evaluate_neighbours() function. Each tile discrete tile position is considered (central, perimiter, corner), and each possible configuration of dead/alive neighbours is considered"""

        #   Test cases A:
        # Tile is modelled as a central tile, and will have 8 neighbours
        for num in range(9):
            test_live_tile = Tile(self.settings, self.screen, live_neigbours=num, dead_neigbours=8-num, colour=self.settings.live_col)
            test_dead_tile = Tile(self.settings, self.screen, live_neigbours=num, dead_neigbours=8-num, colour=self.settings.dead_col)
            test_tiles = [test_live_tile, test_dead_tile]
            gf.evaluate_neighbours(test_tiles, self.settings)
            if num < 2 or num > 3:
                self.assertEqual(test_tiles[0].change_next_turn, True)
            else:
                self.assertEqual(test_tiles[0].change_next_turn, False)
            if num == 3:
                self.assertEqual(test_tiles[1].change_next_turn, True)
            else:
                self.assertEqual(test_tiles[1].change_next_turn, False)


        #   Test cases B:
        # Tile will now be modelled as a perimiter tile, where is has 5 neighbours
        # Same test conditions apply
        for num in range(6):
            test_live_tile = Tile(self.settings, self.screen, live_neigbours=num, dead_neigbours=5-num, colour=self.settings.live_col)
            test_dead_tile = Tile(self.settings, self.screen, live_neigbours=num, dead_neigbours=5-num, colour=self.settings.dead_col)
            test_tiles = [test_live_tile, test_dead_tile]
            gf.evaluate_neighbours(test_tiles, self.settings)
            if num < 2 or num > 3:
                self.assertEqual(test_tiles[0].change_next_turn, True)
            else:
                self.assertEqual(test_tiles[0].change_next_turn, False)
            if num == 3:
                self.assertEqual(test_tiles[1].change_next_turn, True)
            else:
                self.assertEqual(test_tiles[1].change_next_turn, False)


        #   Test cases C:
        # Tile will now be modelled as a corner tile, which only has 3 neighbours
        # Same test conditions apply
        for num in range(4):
            test_live_tile = Tile(self.settings, self.screen, live_neigbours=num, dead_neigbours=3-num, colour=self.settings.live_col)
            test_dead_tile = Tile(self.settings, self.screen, live_neigbours=num, dead_neigbours=3-num, colour=self.settings.dead_col)
            test_tiles = [test_live_tile, test_dead_tile]
            gf.evaluate_neighbours(test_tiles, self.settings)
            if num < 2 or num > 3:
                self.assertEqual(test_tiles[0].change_next_turn, True)
            else:
                self.assertEqual(test_tiles[0].change_next_turn, False)
            if num == 3:
                self.assertEqual(test_tiles[1].change_next_turn, True)
            else:
                self.assertEqual(test_tiles[1].change_next_turn, False)



unittest.main()