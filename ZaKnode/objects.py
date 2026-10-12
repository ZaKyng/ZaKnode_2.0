import pygame
from pygame import Vector2
from . import base
from . import nodes
from . import modifiers
from . import resources

# ----------- Objects ------------ #

class ShowAxis:
    def __init__(self, parentNode : base.Node):
        self.parentNode = parentNode
        self.images = resources.SpriteSheet(parentNode.game.directory("assets/axis.png"), Vector2(15, 15), alpha_channel = True)

        size = Vector2(40, 40)
        gap = 50

        offsets = [Vector2(gap, size.x // -2), Vector2(size.x // -2, gap), Vector2(gap, gap)]
        axis = ["x", "y", None]

        self.tiles = []

        self.tiles.append(nodes.TileMapBlock(self.parentNode, size, self.images, [0, 0], zindex = 600))

        self.hitareas = []
        self.modifiers = []

        for i in range(3):
            self.tiles.append(nodes.TileMapBlock(self.parentNode, size, self.images, [1 + i, 0], zindex = 600, offset = offsets[i]))
            new_area = nodes.CollisionArea(self.parentNode, 98 + i, show = True)
            new_area.addCollisionBlock(size, offset = offsets[i])
            self.hitareas.append(new_area)

            self.modifiers.append(modifiers.MouseDragMove(self.parentNode, 98 + i, axis = axis[i]))


    
    def hide(self):
        for tile in self.tiles:
            tile.kill()
        
        for hitarea in self.hitareas:
            hitarea.kill()

class Button:
    def __init__(self, parentNode, text, func, font_name, font_size = "m", txt_color = (0, 0, 0), bg_color = (255, 255, 255), padding = 0, offset_str = None, offset = Vector2(0, 0), physics_layer = 0, hover_txt_color = None, hover_bg_color = None):
        self.button = nodes.TextBlock(parentNode, text, font_name, font_size = font_size, txt_color = txt_color, bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset)
        play_collision = nodes.CollisionArea(self.button, physics_layer)
        self.collision_block = play_collision.addCollisionBlock(self.button.size)
        modifiers.ClickObject(self.button, physics_layer, func)
        hover_bg_color = hover_bg_color if hover_bg_color is not None else bg_color
        hover_txt_color = hover_txt_color if hover_txt_color is not None else txt_color
        modifiers.Hover(self.button, physics_layer, lambda: self.button.change(bg_color = hover_bg_color, padding = padding + 4, offset_str = offset_str, offset = offset), lambda: self.button.change(bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset))






