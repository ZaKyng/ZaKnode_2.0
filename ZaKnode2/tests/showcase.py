import pygame
from pygame import Vector2
from .. import *

    



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
    scene2 = nodes.Scene("scene2", my_game, bg_color = (20, 200, 100))
    scene3 = nodes.Scene("scene3", my_game, bg_color = (200, 20, 100))
    scene4 = nodes.Scene("scene4", my_game, bg_color = (100, 20, 200))
    scene5 = nodes.Scene("scene5", my_game, bg_color = (60, 50, 60)) 
    scene6 = nodes.Scene("scene6", my_game, bg_color = (200, 190, 20))
    scene7 = nodes.Scene("scene7", my_game, bg_color = (12, 5, 9))
    scene8 = nodes.Scene("scene8", my_game, bg_color = (89, 214, 128))
    scene9 = nodes.Scene("scene9", my_game, bg_color = (0, 0, 0))
    scene10 = nodes.Scene("scene10", my_game, bg_color = (240, 50, 60))
    scene11 = nodes.Scene("scene11", my_game, bg_color = (200, 220, 240))
    scene12 = nodes.Scene("scene12", my_game)

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
    

    parent2 = nodes.BaseNode(scene2, offset_str = "CenTer")
    block2 = nodes.SpriteBlock(parent2, (250, 250), bonsai.image, offset_str = "center")
    objects.ShowAxis(parent2)
    objects.ShowAxis(block2)
    modifier2 = modifiers.KeyboardWASDMove(parent2, 320, leave_window=True)

    desc2 = nodes.TextBlock(scene2, "Image loading and move with WASD", my_game.fonts.fonts["default"], "l", offset_str="top", txt_color = (0, 0, 0), bg_color = (255, 255, 255), padding = 25, zindex = 2)


    parent3 = nodes.BaseNode(scene3, offset_str = "center", offset = Vector2(250, 0), zindex = -1)
    block3 = nodes.AnimatedSpriteBlock(parent3, (250, 250), bonsai_grow_anim.frames, 1.5, offset_str = "center")
    modifier3 = modifiers.MouseClickMove(parent3)

    desc3 = nodes.TextBlock(scene3, "2 animations from once loaded tilemap image", my_game.fonts.fonts["default"], "s", offset_str = "top", txt_color = (0, 0, 0), bg_color = (255, 255, 255), padding = 15)
    desc4 = nodes.TextBlock(scene3, "Sorted by z-index and 1 moves on mouse click", my_game.fonts.fonts["default"], "s", offset_str = "top", offset = Vector2(0, 120), txt_color = (200, 200, 240), bg_color = (12, 12, 12), padding = 25, zindex = -1)

    parent4 = nodes.BaseNode(scene3, offset_str = "center", offset = Vector2(-250, 0))
    block4 = nodes.AnimatedSpriteBlock(parent4, (250, 250), bonsai_color_anim.frames, 3, offset_str = "center")

    parent5 = nodes.BaseNode(scene4)
    block5 = nodes.TileMapBlock(parent5, (250, 250), bonsai_grid, [1, 1])
    modifier5 = modifiers.LinearMove(parent5, Vector2(0, 0), Vector2(800, 540))

    explain_text = nodes.Label(scene4, "Explanation: ", my_game.fonts.fonts["default"], font_size = "s", color = (200, 200, 200), zindex = 8, offset_str = "top-right", offset = Vector2(-20, 20))
    explain = nodes.SpriteBlock(scene4, Vector2(300, 300), bonsai.image, zindex = 5, offset_str = "top-right", offset = Vector2(-20, 20 + explain_text.size.y))
    explain_box = nodes.SpriteBlock(explain, explain.size // 3, box.image, zindex = 6)
    

    modifiers.ForeverDo(explain_box, lambda: explain_box.change(offset = Vector2(explain_box.size[0] * block5.coords[0], explain_box.size[1] * block5.coords[1])))

    press = modifiers.PressKey(scene4, pygame.K_a, lambda: block5.change(coords_change = [1, 0]))
    press = modifiers.PressKey(scene4, pygame.K_s, lambda: block5.change(coords_change = [0, 1]))
    press = modifiers.PressKey(scene4, pygame.K_d, lambda: block5.change(coords_change = 1))

    desc5_1 = nodes.TextBlock(scene4, "Press A, S or D to change", my_game.fonts.fonts["default"], "s", (255, 200, 255), (25, 25, 25), padding = 18, offset = Vector2(130, 20))
    desc5 = nodes.Label(scene4, "Translation of one tile of a tilemap \nfrom 1 point to another", my_game.fonts.fonts["default"], "l", (220, 240, 190), offset_str = "bottom-left", offset = Vector2(10 * my_game.vw, 0))


    tile5 = nodes.TileMapBlock(scene5, Vector2(400, 500), bonsai_grid, [0, 0], offset_str = "center")
    collision_tile5 = nodes.CollisionArea(tile5, 2, show_self = True)
    collision_tile5.change(show = True)
    collision_tile5.addCollisionBlock(tile5.size, offset = Vector2(100, 200))
    modifiers.ClickObject(tile5, 2, lambda: tile5.change(coords_change = 1))
    drag = modifiers.MouseDragMove(tile5, 2)
    desc6 = nodes.Label(scene5, "Click on green area (hitbox) to change image", my_game.fonts.fonts["default"], "l", (110, 100, 255), offset_str = "bottom")

    parent6 = nodes.BaseNode(scene6)
    objects.ShowAxis(parent6)
    rotating_block = nodes.ColorBlock(parent6, Vector2(100, 100), pygame.Color(0, 0, 240), offset_str = "center")
    modifiers.SignalTrigger(rotating_block, "change_color", lambda: rotating_block.change(offset = rotating_block.offset - Vector2(20, 0)))
    circle = modifiers.CircularMove(parent6, Vector2(my_game.size) // 2, radius = 350, speed = 50, clockwise = False, start_deg = 180, show_path = True)

    

    modifiers.PressKey(scene6, pygame.K_d, lambda: circle.change(radius = circle.radius + 10))
    modifiers.PressKey(scene6, pygame.K_f, lambda: circle.change(radius = circle.radius - 10))
    modifiers.PressKey(scene6, pygame.K_g, lambda: circle.change(speed = circle.speed + 10))
    modifiers.PressKey(scene6, pygame.K_h, lambda: circle.change(speed = circle.speed - 10))
    modifiers.PressKey(scene6, pygame.K_j, lambda: circle.change(clockwise = circle.direction == -1))

    fx_player = modifiers.SoundEffectPlayer(scene9)
    fx_player.add("click", click_fx.sound)
    modifiers.PressKey(scene9, pygame.K_SPACE, lambda: fx_player.play("click"))

    nodes.TextBlock(scene6, "Move block with axis and move its modifiers with it", my_game.fonts.fonts["default"], "s", txt_color = (210, 100, 255), padding = 20, offset_str = "Top")
    nodes.Label(scene6, "Press D, F, G, H or J to change properties", my_game.fonts.fonts["default"], "l", (10, 80, 55), offset_str = "bottom")


    block_size = 2
    for i in range(int(my_game.size.x) // block_size):
        new_block = nodes.ColorBlock(scene7, Vector2(block_size, block_size), color = (255 / (my_game.size.x // block_size) * i, 255 / (my_game.size[0] // block_size) * i / 2, 255), offset = Vector2(i * block_size, 200))
        modifiers.AxisMove(new_block, my_game.size.y - block_size - 200, axis = "y", mode = "ease-both", speed = 300 + i, strength = 1.5)

    nodes.Label(scene7, f"{int(my_game.size.x // block_size)} blocks with different speeds", my_game.fonts.fonts["default"], "l", (10, 80, 55), offset_str = "bottom")

    block_to_follow = nodes.TileMapBlock(scene8, Vector2(150, 150), bonsai_grid, [1, 2], offset = Vector2(-400, 0))
    objects.ShowAxis(block_to_follow)
    modifiers.CircularMove(block_to_follow, Vector2(400, 0), speed = 220)
    centralize_test = nodes.ColorBlock(block_to_follow, Vector2(100, 100), color = (250, 0, 250), offset = (200, 100))
    center_mod = modifiers.Centralize(block_to_follow, scene8)
    objects.ShowAxis(scene8)
    modifiers.PressKey(scene8, pygame.K_d, lambda: center_mod.kill())
    following_block = nodes.ColorBlock(scene8, Vector2(120, 120), color = (100, 0, 240), zindex = 1)
    modifiers.Follow(following_block, block_to_follow)
    
    block_size = 2
    square_num = int(my_game.size.x) // block_size
    for i in range(square_num):
        new_block = nodes.ColorBlock(scene9, Vector2(block_size, block_size), color = (255 / (my_game.size.x // block_size) * i, 255 / (my_game.size[0] // block_size) * i / 2, 255), offset = Vector2(i * block_size, (my_game.size.y - block_size) / 2))
        if i == 0:
            modifiers.AxisMove(new_block, start = 200, end = my_game.size.y - block_size - 200, axis = "y", mode = "ease-both", speed = square_num + 5, strength = 1.5)
        else:
            modifiers.Follow(new_block, last_block, axis = "y", speed = square_num + 5 - i)
        last_block = new_block

    nodes.Label(scene9, f"{int(my_game.size.x // block_size)} blocks with different speeds (Version 2)", my_game.fonts.fonts["default"], "l", (10, 80, 55), offset_str = "bottom")

    combined_offset = 5
    for font_key in list(my_game.fonts.fonts["default"]["font"].keys()):
        last_block = nodes.TextBlock(scene10, f"Font sizes {font_key}", my_game.fonts.fonts["default"], font_size = font_key, txt_color = (50, 240, 230), bg_color = (80, 100, 90), padding = 9, offset_str = "top", offset = (0, combined_offset))
        combined_offset += last_block.size.y + 10

    half_screen = nodes.ColorBlock(scene11, Vector2(my_game.screen_size.x / 2, my_game.screen_size.y), (15, 30, 80), offset_str = "left")
    
    final_test1 = nodes.TileMapBlock(scene11, Vector2(200, 200), bonsai_grid, [1, 2], offset_str = "center", zindex = 1)
    
    modifi_test1 = modifiers.ForeverDo(final_test1, lambda: final_test1.change(angle = final_test1.angle - 1, offset_str = "center"))

    modifiers.PressKey(scene11, pygame.K_k, lambda: modifi_test1.change(active = not modifi_test1.active))

    modifiers.PressKey(scene11, pygame.K_d, lambda: final_test1.change(coords_change = 1))


    tile_positioner = nodes.BaseNode(scene12, offset = (-25, -25))
    tile_map_test = nodes.TileMap(tile_positioner, bonsai_grid, Vector2(50, 50))

    layer1 = tile_map_test.addLayer()

    tiles = [
        [0, 0],
        [0, 1],
        [1, 0],
        [2, 2]
    ]

    for position in tiles:
        layer1.addTile(position, [0, 1])

    modifiers.PressKey(tile_map_test, pygame.K_r, lambda: tile_map_test.change(one_tile_size = tile_map_test.tile_size + Vector2(2, 2)))

    
    music_player = modifiers.MusicPlayer(scene12)

    music_player.add("theme", looping_music)

    scene12.change(onEntry = lambda: music_player.play("theme"), onExit = lambda: music_player.stop("theme"))

    

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