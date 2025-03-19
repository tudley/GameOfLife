from settings import Settings
import game_functions

settings = Settings()
print(settings.screen_width)
print(settings.tile_width * settings.cols)

print(settings.screen_height)
print(settings.tile_height * settings.rows + settings.button_height)
print(settings.button_top)