import pygame
from pygame import Vector2
from . import *

    



# ----- Pygame setup ----- #
def run():
    window_size = (1600, 900)
    my_game = nodes.Game(window_size, __file__, fps = 120, screen_ratio = 16/9, overflow_hidden = True)
    my_game.fonts.addFont("default", my_game.directory("assets/font1.ttf"))

    bonsai = resources.Image(my_game.directory("assets/bonsai.png"), alpha_channel = True)

    bonsai_grid = resources.SpriteSheet(my_game.directory("assets/bonsai.png"), Vector2(32, 32), alpha_channel = True)

    bonsai_grow_anim = resources.Animation(bonsai_grid.grid, 0, 5)
    bonsai_color_anim = resources.Animation(bonsai_grid.grid, 5, 7)

    box = resources.Image(my_game.directory("assets/box.png"), True)

    click_fx = resources.Sound(my_game.directory("assets/click.mp3"))

    looping_music = resources.Sound(my_game.directory("assets/looping_music.mp3"))

    # --- Level-- #

    default = nodes.Scene("default", my_game)
    scene1 = nodes.Scene("scene1", my_game, bg_color = (200, 100, 20))

    objects.ShowAxis(default)

    desc1 = nodes.Label(default, "Use <- / -> to switch scenes", my_game.fonts.fonts["default"], font_size = "l",  offset_str="center")
    press_esc = nodes.Label(default, "Press ESC to exit", my_game.fonts.fonts["default"], offset_str = "bottom-right")


    parent1 = nodes.BaseNode(scene1, offset = Vector2(150, 150))
    objects.ShowAxis(parent1)
    block1 = nodes.ColorBlock(parent1, (80, 80), (170, 200, 20, 90), alpha_channel = True)
    block1_2 = nodes.ColorBlock(parent1, (80, 80))
    block1_3 = nodes.ColorBlock(parent1, (80, 80), offset = Vector2(100, 0))
    
    modifier1_1 = modifiers.AxisMove(block1, 0, 700, speed = 100, mode = "linear", strength = 6, show_path = True)
    modifier1_2 = modifiers.AxisMove(block1_2, 0, 700, speed = 300, mode = "ease-in", strength = 0.6)
    modifier1_22 = modifiers.AxisMove(block1_3, 0, 700, speed = 300, axis = "y", mode = "ease-out", strength = 12, show_path = True)

    modifier1_2.change(axis = "y")

    objects.ShowAxis(block1)

    collision = nodes.CollisionArea(block1, 8, show = True)
    collision.addCollisionBlock(Vector2(20, 200), offset = Vector2(100, 100))
    my_game.signals.addSignal("change_color")
    modifier1_3 = modifiers.ClickObject(block1, 8, lambda: my_game.signals.setOffSignal("change_color"))

    desc = nodes.TextBlock(scene1, "Visible axis can change objects position", my_game.fonts.fonts["default"], "m", offset_str="bottom", offset = Vector2(0, -120))
    desc_1 = nodes.TextBlock(scene1, "Red line shows the path of AxisMove", my_game.fonts.fonts["default"], "m", offset_str="bottom", offset = Vector2(0, -80))
    desc1 = nodes.Label(scene1, "Showcase of linear and gradual interpolation on block of color", my_game.fonts.fonts["default"], font_size = "l", offset_str="top")

    press_global = []
    for scene in list(my_game.scenes.scenes.values()):
        press_global.append(modifiers.PressKey(scene, pygame.K_RIGHT, lambda: my_game.scenes.changeScene()))
        press_global.append(modifiers.PressKey(scene, pygame.K_LEFT, lambda: my_game.scenes.changeScene(-1)))


    def scene_changing(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                my_game.end()

            if event.key == pygame.K_UP:
                my_game.scenes.changeScene(-1)
                
            elif event.key == pygame.K_DOWN:
                my_game.scenes.changeScene()
        
        """if event.type == pygame.MOUSEBUTTONDOWN:

            position_in_screen = Vector2(event.pos) - my_game.scenes.scenes[my_game.scenes.current_scene].position
            mouse = Vector2(int(position_in_screen.x / my_game.scale.x), int(position_in_screen.y / my_game.scale.y))"""


    def test():
        pass

    my_game.run(test, global_input = scene_changing)


if __name__ == "__main__":
    run()