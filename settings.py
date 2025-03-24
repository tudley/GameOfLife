class Settings():
    def __init__(self):

        #screen settings
        self.screen_width = 800
        self.screen_height = 1000
        self.bg_colour = (0, 0, 0)

        # frame settings
        self.frame = 0
        self.highest_frame = 0

        self.frame_counter_left = 0
        self.frame_counter_top = 0
        self.frame_counter_width = self.screen_width
        self.frame_counter_height = 50
        self.frame_counter_colour = (120, 120, 120)


        # rows and collumns
        self.rows = 20
        self.cols = 20

        #play button settings
        self.button_height = 75
        self.button_width1 = self.screen_width / 3
        self.button_width2 = self.button_width1 / 2
        self.button_left = 0

        #tile settings
        self.live_col = (255, 255, 255)
        self.dead_col = (0, 0, 0)
        self.tile_perimiter = 0
        self.tile_width = self.screen_width / self.cols
        self.tile_height = (self.screen_height - ((2 * self.button_height) + self.frame_counter_height)) / self.rows


        self.button_top1 = (self.rows * self.tile_height) + self.frame_counter_height
        self.button_top2 = (self.rows * self.tile_height) + self.button_height + self.frame_counter_height


        #set flag for game status
        self.active = False

        #set the sleep interval
        self.sleep_timer = 0.1

        # dictionary to store tile configuration for each frame
        self.frame_tile_config_dict = {}

        # config for export option menus
        self.exporting = False
        
        
        self.box_left = self.screen_width/6
        self.box_top = self.screen_height/3
        self.box_width = 2 * self.screen_width / 3
        self.box_height = self.screen_height/3
        self.box_button_top = self.box_top + self.box_height/2
        self.box_perimiter1 = self.box_width / 20
        self.box_button_width = (self.box_width - (3 * self.box_perimiter1)) / 2
        self.text_top = self.box_top + self.box_height/4
        self.text_height = self.box_height/4
        self.user_text = ''
        self.user_typing = False






