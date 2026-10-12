import pygame
from ZaKnode import *

# ----- Pygame setup ----- #
def run():
    screen_size = (1980, 1080)
    my_game = nodes.Game(screen_size, __file__, fps = 120)

    def global_input(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                my_game.end()
        pass

    def test():
        pass

    my_game.run(test, global_input = global_input)

if __name__ == "__main__":
    run()