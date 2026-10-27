import pygame
from ZaKnode2 import *

# ----- Pygame setup ----- #
def run():
    screen_size = (400, 200)
    simulation_size = (screen_size[0] * 2, screen_size[1] * 2)
    my_game = nodes.Game(screen_size, __file__, fps = 120, simulation_size = simulation_size)

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