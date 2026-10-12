import os
import sys
import json
import pygame
from pygame import Vector2
from pygame import Color

from .base import Node
from . import modifiers
from . import resources


"""
class default(Node):
    def __init__(self, parentNode, size, zindex : float = 0, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex)

        self.change(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = True)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)

    def change(self, size = None, offset_str = None, offset = None, zindex = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)
        
    def kill(self):
        super().kill()
"""
# ----------- Nodes ------------ #

#   # -- Primary -- #

class Game:
    def __init__(self, 
                    window_size : tuple, 
                    file_location, 
                    name : str = "ZaKgame window", 
                    fps : int = 120, 
                    simulation_size : tuple = None,
                    relative_icon_path : str = None,
                    fullscreen : bool = False):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.file = file_location

        self.running = True

        self.offset = Vector2(0, 0)
        self.position = Vector2(0, 0)

        self.game = self
        
        self.fonts = FontManager(self)
        self.signals = SignalManager(self)
        self.scenes = SceneManager(self)
        
            
        self.window_size = Vector2(window_size)
        self.window_ratio = self.window_size.x / self.window_size.y
        self.window_atr = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE

        if simulation_size is None:
            simulation_size = self.window_size
        self.simulation_size = Vector2(simulation_size)
        self.size = self.simulation_size
        self.simulation_ratio = self.simulation_size.x / self.simulation_size.y
        self.canvas = pygame.Surface(self.simulation_size)

        self.vw = self.simulation_size.x / 100
        self.vh = self.simulation_size.y / 100

        Scene(self.scenes.default_scene_name, self)

        pygame.display.set_caption(name)

        if relative_icon_path:
            pygame.display.set_icon(pygame.image.load(self.directory(relative_icon_path)))

        self.windowResize(self.size)

        self.clock = pygame.time.Clock()

        self.tick_speed = fps

        self.delta = 1 / fps

    
    def run(self, func = None, global_input : callable = None):
        while self.running:
            dt_ms = self.clock.tick(self.tick_speed)
            self.delta = dt_ms / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:
                    self.windowResize(Vector2(event.size))

                if global_input:
                    global_input(event)
            
                self.scenes.scenes[self.scenes.current_scene].event(event)

            if func:
                func()

            self.screen.fill((0, 0, 0))

            self.scenes.scenes[self.scenes.current_scene].update()
            self.draw()

            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def end(self):
        self.running = False
    
    def directory(self, src : str):
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(self.file))

        #return os.path.join(base_path, src)
        return os.path.normpath(os.path.join(base_path, src))

    def windowResize(self, new_size):
        self.signals.setOffSignal("window_size_changed")
    
        self.window_size = new_size
        self.window_ratio = self.window_size.x / self.window_size.y
        self.screen = pygame.display.set_mode(self.window_size, self.window_atr)


        wider = self.window_ratio > self.simulation_ratio
        
        if wider:
            self.canvas_size = Vector2(self.window_size.y * self.simulation_ratio, self.window_size.y)
            self.canvas_position = Vector2((self.window_size.x - self.window_size.y * self.simulation_ratio) / 2, 0)
        else:
            self.canvas_size = Vector2(self.window_size.x,self.window_size.x / self.simulation_ratio)
            self.canvas_position = Vector2(0, (self.window_size.y - self.window_size.x / self.simulation_ratio) / 2)

    def nothing(self):
        pass

    def draw(self):
        self.canvas.fill((0, 0, 0))
        self.canvas = self.scenes.scenes[self.scenes.current_scene].draw(self.canvas)

        self.screen.blit(pygame.transform.scale(self.canvas, self.canvas_size), self.canvas_position)

class FontManager:
    def __init__(self, game = Game):
        self.game = game
        self.fonts = {}
        
    def addFont(self, name, path, size : float = 2):
        font_sizes = {"xs" : int(size * self.game.vh), "s" : int((size + 1) * self.game.vh), "m" : int((size + 2) * self.game.vh), "l" : int((size + 3) * self.game.vh), "xl" : int((size + 4) * self.game.vh)}
        new_font = {}
        new_font["raw-font"] = path
        new_font["size"] = size
        new_font["font"] = {}
        for key in font_sizes.keys():
            new_font["font"][key] = pygame.font.Font(path, font_sizes[key])
        self.fonts[name] = new_font

    def updateFont(self, name):
        font_sizes = {"xs" : int(self.fonts[name]["size"] * self.game.vh),
                      "s" : int((self.fonts[name]["size"] + 1) * self.game.vh),
                      "m" : int((self.fonts[name]["size"] + 2) * self.game.vh),
                      "l" : int((self.fonts[name]["size"] + 3) * self.game.vh),
                      "xl" : int((self.fonts[name]["size"] + 4) * self.game.vh)
                      }
        if self.fonts[name]["raw-font"] is not None:
            for key in self.fonts[name]["font"].keys():
                if key != "raw-font" and key != "size":
                    self.fonts[name]["font"][key] = pygame.font.Font(self.fonts[name]["raw-font"], font_sizes[key])

class SignalManager:
    def __init__(self, game = Game):
        self.game = game
        self.signals = {}
    
    def addSignal(self, name):
        self.signals[name] = False
    
    def setOffSignal(self, name):
        self.signals[name] = True

class SceneManager:
    def __init__(self, game = Game):
        self.game = game
        self.scenes = {}
        self.game.signals.addSignal("scene_changed")

        self.default_scene_name = "empty"
        self.current_scene = None

    
    def addScene(self, name : str, scene):
        self.scenes[name] = scene
        if not self.current_scene:
            self.current_scene = name
        elif self.current_scene == self.default_scene_name and name != self.default_scene_name:
            self.current_scene = name
            self.scenes.pop(self.default_scene_name)
        
    def changeScene(self, changer = None):
        if isinstance(changer, str):
            last = self.current_scene

            if changer in self.scenes:
                if self.scenes[changer].active:
                    self.exitScene(self.scenes[self.current_scene])
                    self.current_scene = changer
                    self.enterScene(self.scenes[self.current_scene])
            else:
                print("error")

        elif isinstance(changer, int):
            scene_names = list(self.scenes.keys())
            index = scene_names.index(self.current_scene)
            index += changer
            
            index = index % len(scene_names)

            if self.scenes[scene_names[index]].active:
                self.exitScene(self.scenes[self.current_scene])

                self.current_scene = scene_names[index]

                self.enterScene(self.scenes[self.current_scene])
            else:
                self.changeScene(changer + 1 if changer > 0 else changer - 1)
        else:
            self.changeScene(1)
        self.game.signals.setOffSignal("scene_changed")
        
    def enterScene(self, scene):
        if scene.onEntry is not None:
            scene.onEntry()

    def exitScene(self, scene):
        if scene.onExit is not None:
            scene.onExit()

    def removeScene(self, name):
        self.scenes.pop(name)

class Scene(Node):
    def __init__(self, name : str, game : Game, bg_color = Color(0, 0, 0), onEntry : callable = None, onExit : callable = None):
        self.game = game

        self.parentNode = game

        self.children = []
        self.collision = []
        
        self.name = name
        self.game.scenes.addScene(self.name, self)

        self.onEntry = None
        self.onExit = None

        self.change(Color(bg_color), self.game.simulation_size, offset_str = "center", offset = Vector2(0, 0), onEntry = onEntry, onExit = onExit, active = True)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas.blit(self.surface, self.position)

        canvas = super().draw(canvas)

        return canvas
    
    def kill(self):
        for child in self.children[:]:
            child.kill()

        self.children.clear()
        self.collision.clear()

        self.game.removeScene(self.name)
    
    def addChild(self, newChild):
        super().addChild(newChild)

    def change(self, bg_color = None, size = None, offset_str = None, offset = None, onEntry = None, onExit = None, active = None):
        if bg_color is not None:
            self.bg_color = bg_color
            try:
                self.surface.fill(self.bg_color)
            except:
                pass
        
        if onEntry is not None:
            self.onEntry = onEntry
        
        if onExit is not None:
            self.onExit = onExit
        
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, active = active)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.bg_color)
        
class BaseNode(Node):
    def __init__(self, parentNode,  zindex : float = 0, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, size = Vector2(0, 0), zindex = zindex, offset_str = offset_str, offset = offset, active = True)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def change(self, offset_str = None, offset = None, zindex = None, active = None, sizer = None):
        if sizer is not None:
            self.change(offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

        super().nodeChange(offset_str = offset_str, offset = offset, zindex = zindex, active = active)

    def kill(self):
        super().kill()

class PredrawnCanvas(Node):
    def __init__(self, parentNode, size, zindex : float = 0, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex)

        self.change(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = True)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas.blit(self.canvas, self.position)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)

    def change(self, size = None, offset_str = None, offset = None, zindex = None, active = None):
        if size is not None:
            self.canvas = pygame.Surface(size, pygame.SRCALPHA)
        self.redrawCanvas()
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)
        
    def kill(self):
        super().kill()


    def redrawCanvas(self):
        self.canvas.fill((0, 0, 0, 0))

        self.canvas = super().draw(self.canvas)

#   # -- Logic -- #

class CollisionArea(Node):
    def __init__(self, parentNode, physics_layer : int = 0, show : bool = False, show_self : bool = False):
        super().__init__(parentNode, size = parentNode.size, zindex = 100, offset_str = None, offset = Vector2(0, 0))
        
        self.collision_blocks = []
        
        self.change(physics_layer = physics_layer, show = show, show_self = show_self, active = True)

        self.parentNode.collision.append(self)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas : pygame.surface):
        if self.show_self:
            canvas.blit(self.surface, self.position)
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def change(self, physics_layer : int = None, show : bool = None, show_self : bool = None, size : Vector2 = None, offset_str : str = None, offset = None, zindex : int = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if physics_layer is not None:
             self.physics_layer = physics_layer

        if show is not None:
            self.show = show
        
        if show_self is not None:
            self.show_self = show_self
            if self.show_self:
                self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
                self.surface.fill("#ff00ff44")
        
        if self.show_self and size is not None:
            self.surface = pygame.Surface(size, pygame.SRCALPHA)
            self.surface.fill("#ff00ff44")


    def kill(self):
        for block in self.collision_blocks:
            block.kill()
        super().kill()
    

    def addCollisionBlock(self, size : Vector2, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        return CollisionBlock(self, size, offset_str = offset_str, offset = offset)

class CollisionBlock(Node):
    def __init__(self, parentNode : CollisionArea, size : Vector2, zindex : float = -5, offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
        self.parentNode.collision_blocks.append(self)

        self.change()
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        
    def draw(self, canvas : pygame.surface):
        if self.parentNode.show:
            canvas.blit(self.surface, self.position)
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def change(self, size = None, offset_str = None, offset = None, zindex = None, sizer = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex)

        self.rect = pygame.Rect(self.position, self.size)
        if self.parentNode.show:
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
            self.surface.fill("#00ff0044")

        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

    def kill(self):
        self.parentNode.collision_blocks.remove(self)
        super().kill()


#   # -- Visuals -- #

class Label(Node):
    def __init__(self, parentNode, text : str, font_name : str, font_size : str = "m", color : Color = Color(255, 255, 255), zindex : float = 0, 
                offset_str : str = None, offset : Vector2 = Vector2(0, 0)):
        super().__init__(parentNode, zindex = zindex, offset_str = offset_str, offset = offset)
        self.change(text = text, font_name = font_name, font_size = font_size, color = color, offset_str = offset_str, offset = offset, active = True)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        
    def draw(self, canvas : pygame.surface):
        canvas.blit(self.surface, self.position)
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def change(self, text : str = None, font_name : str = None, font_size = None, color : Color = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        if text is not None:
            self.text = text
        
        if font_name is not None:
            try:
                self.font = self.game.fonts.fonts[font_name]
            except:
                self.font = self.game.fonts.fonts["default"]
        
        if font_size is not None:
            self.font_size = font_size

        if color is not None:
            self.color = Color(color)

        if text is not None or color is not None or font_name is not None or font_size is not None:
            try:
                self.message = self.font["font"][self.font_size].render(self.text, True, self.color)
            except:
                self.message = self.font["font"]["m"].render(self.text, True, self.color)

            self.surface = pygame.Surface(self.message.get_size(), pygame.SRCALPHA)

            self.surface.blit(self.message)

            self.size = Vector2(self.surface.get_size())

        if sizer is not None:
            self.change(font_size = self.font_size, offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

        super().nodeChange(offset_str = offset_str, offset = offset, zindex = zindex, active = active)


    def kill(self):
        super().kill()

class TextBlock(Node):
    def __init__(self, parentNode, text : str, font_name : str, font_size : str = "m", txt_color = Color(255, 255, 255), bg_color = Color(0, 0, 0), padding = 0, zindex = 0, 
                offset_str = None, offset = Vector2(0, 0), alpha_channel = False):
        super().__init__(parentNode, offset_str = offset_str, offset = offset, zindex = zindex)
        
        self.change(text = text, font_name = font_name, font_size = font_size, txt_color = txt_color, bg_color = bg_color, padding = padding, offset_str = offset_str, offset = offset, zindex = zindex, alpha_channel = alpha_channel, active = True)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        

    def draw(self, canvas : pygame.surface):
        canvas.blit(self.surface, self.position)
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def change(self, text = None, font_name : str = None, font_size = None, txt_color = None, bg_color = None, padding = None, offset_str = None, offset = None, zindex = None, alpha_channel = None, sizer = None, active = None):
        relevant_change = False
        
        if text is not None:
            self.text = text
            relevant_change = True
        
        if font_name is not None:
            try:
                self.font = self.game.fonts.fonts[font_name]
            except:
                self.font = self.game.fonts.fonts["default"]
            relevant_change = True
        
        if font_size is not None:
            self.font_size = font_size
            relevant_change = True

        if txt_color is not None:
            self.color = Color(txt_color)
            relevant_change = True
        
        if bg_color is not None:
            self.background = Color(bg_color)
            relevant_change = True
        
        if padding is not None:
            self.padding = padding
            relevant_change = True

        if alpha_channel is not None:
            self.alpha = alpha_channel
            relevant_change = True

        if relevant_change:
            try:
                self.message = self.font["font"][self.font_size].render(self.text, True, self.color)
            except:
                self.message = self.font["font"]["m"].render(self.text, True, self.color)

            if self.alpha:
                self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                        self.message.get_size()[1] + self.padding * 2), pygame.SRCALPHA)
            else:
                self.surface = pygame.Surface((self.message.get_size()[0] + self.padding * 2, 
                                        self.message.get_size()[1] + self.padding * 2))
                
            self.surface.fill(self.background)
            self.surface.blit(self.message, (self.padding, self.padding))

            self.size = Vector2(self.surface.get_size())

        if sizer is not None:
            self.change(font_size = self.font_size, offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

        super().nodeChange(offset_str = offset_str, offset = offset, zindex = zindex, active = active)


    def kill(self):
        super().kill()

class ColorBlock(Node):
    def __init__(self, parentNode, size, color = Color(255, 255, 255, 255), zindex = 0, offset_str = None, offset = Vector2(0, 0), alpha_channel = False):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex)

        self.angle = 0
        self.change(size = size, color = color, alpha_channel = alpha_channel, active = True)


    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()
        
    def draw(self, canvas : pygame.surface):
        canvas.blit(self.surface, self.position)
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)
    
    def change(self, size = None, color = None, alpha_channel = None, angle = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if size is not None:
            self.orig_size = self.size

        if color is not None:
            self.color = Color(color)
        
        if alpha_channel is not None:
            self.alpha_channel = alpha_channel

        if size is not None or alpha_channel is not None:
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA if self.alpha_channel else 0)
        
        if size is not None or color is not None:
            self.surface.fill(self.color)

        if angle is not None:
            self.angle = angle
        
        if angle is not None or size is not None or color is not None:
            self.surface = pygame.Surface(self.orig_size, pygame.SRCALPHA)
            self.surface.fill(self.color)
            self.surface = pygame.transform.rotate(self.surface, self.angle)
            super().nodeChange(size = Vector2(self.surface.get_size()), offset_str = offset_str, offset = offset)
        
        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))
        
        
    
    def kill(self):
        super().kill()

class SpriteBlock(Node):
    def __init__(self, parentNode, size, image, angle : int = None, zindex = 0, offset_str = None, offset = Vector2(0, 0)):
        super().__init__(parentNode, size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = True)
        
        if angle is not None:
            self.change(image = image, angle = angle, offset_str = offset_str, offset = offset)
        else:
            self.angle = 0
            self.change(image = image)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas.blit(self.surface, self.position)
        canvas = super().draw(canvas)

        return canvas

    def addChild(self, newChild):
        super().addChild(newChild)
    
    def kill(self):
        super().kill()

    def change(self, image = None, size = None, angle = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if image is not None:
            self.orig_image = image
            self.orig_size = self.size
            self.surface = pygame.transform.scale(self.orig_image, self.size)

        elif size is not None:
            self.orig_size = self.size
            self.surface = pygame.transform.scale(self.orig_image, self.size)
            if self.angle != 0:
                angle = self.angle
        
        if angle is not None:
            self.angle = angle
        
        if angle is not None or size is not None:
            self.surface = pygame.transform.scale(self.orig_image, self.orig_size)
            self.surface = pygame.transform.rotate(self.surface, self.angle)

            super().nodeChange(size = Vector2(self.surface.get_size()), offset_str = offset_str, offset = offset)

        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))

class AnimatedSpriteBlock(Node):
    def __init__(self, parentNode, size, framesArr, fps, angle = None, zindex = 0, offset_str = None, offset = pygame.Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset, active = True)

        self.frames = []

        if angle is not None:
            self.change(frames_arr = framesArr, fps = fps, angle = angle, offset_str = offset_str, offset = offset)
        else:
            self.angle = 0
            self.change(frames_arr = framesArr, fps = fps)

    def event(self, event):
        super().event(event)
    
    def update(self):
        self.count += 1 * self.game.delta
        if self.count >= self.frameLen:
            self.count = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
        
        self.frame = self.frames[self.index]
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas.blit(self.frame, self.position)
        canvas = super().draw(canvas)

        return canvas

    def addChild(self, newChild):
        super().addChild(newChild)

    def change(self, frames_arr = None, fps = None, angle = None, size = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if frames_arr is not None:
            self.frames.clear()
            for one_frame in frames_arr:
                frame = pygame.transform.scale(one_frame, self.size)
                self.frames.append(frame)
            
            self.frame = self.frames[0]
            
            self.count = 0
            self.index = 0
        
        if size is not None:
            temp = []
            for one_frame in self.frames:
                temp.append(pygame.transform.scale(one_frame, self.size))
            self.frames = list(temp)
        
        if fps is not None:
            self.fps = fps
        
        if angle is not None:
            self.angle = angle
            temp = []
            for one_frame in self.frames[:]:
                temp.append(pygame.transform.rotate(one_frame, angle))
            
            self.frames = temp
            super().nodeChange(size = self.frames[0].get_size(), offset_str = offset_str, offset = offset)
        
        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))
        
        self.frameLen = self.game.tick_speed / (self.fps * 100)
        

    def kill(self):
        super().kill()

class TileMapBlock(Node):
    def __init__(self, parentNode, size, tile_node, coords, zindex = 0, offset_str=None, offset = pygame.Vector2(0, 0)):
        super().__init__(parentNode, size = size, zindex = zindex, offset_str = offset_str, offset = offset)
        
        self.angle = 0
        self.change(tile_node = tile_node, coords = coords, size = size, active = True)


    def event(self, event):
        super().event(event)
    
    def update(self):
        
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas.blit(self.surface, self.position)
        canvas = super().draw(canvas)

        return canvas

    def addChild(self, newChild):
        super().addChild(newChild)

    def change(self, tile_node = None, coords = None, coords_change = None, size = None, angle = None, offset_str = None, offset = None, zindex = None, sizer = None, active = None):
        super().nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex, active = active)

        if size is not None:
            self.orig_size = self.size.copy()

        if tile_node is not None:
            self.tileNode = tile_node
    
        if coords is None:
            if coords_change is not None:
                if isinstance(coords_change, int):
                    new_x = int((self.coords[0] + coords_change) % self.tileNode.tileCount[0])
                    new_y = int((self.coords[1] + (self.coords[0] + coords_change) // self.tileNode.tileCount[0]) % self.tileNode.tileCount[1])
                else:
                    new_x = int((self.coords[0] + coords_change[0]) % self.tileNode.tileCount[0])
                    new_y = int((self.coords[1] + coords_change[1]) % self.tileNode.tileCount[1])
                self.coords = [new_x, new_y]
        else:
            self.coords = [int(coords[0] % self.tileNode.tileCount[0]), int(coords[1] % self.tileNode.tileCount[1])]
        
        if tile_node is not None or coords is not None or coords_change is not None:
            self.surface = self.tileNode.grid[self.coords[0]][self.coords[1]]
            self.orig_image = self.surface

        if size is not None:
            self.surface = pygame.transform.scale(self.surface, self.size)
        
        if angle is not None:
            self.angle = angle
        
        if angle is not None or size is not None or coords is not None or coords_change is not None:
            self.surface = pygame.transform.scale(self.orig_image, self.orig_size)
            self.surface = pygame.transform.rotate(self.surface, self.angle)

            super().nodeChange(size = Vector2(self.surface.get_size()), offset_str = offset_str, offset = offset)

    
        if sizer is not None:
            self.change(size = Vector2(self.size.x * sizer.x, self.size.y * sizer.y), offset = Vector2(self.offset.x * sizer.x, self.offset.y * sizer.y))


    def kill(self):
        super().kill()

class TileMap(Node):
    def __init__(self, parentNode, tile_node, one_tile_size, zindex : float = 0):
        super().__init__(parentNode, size = Vector2(0, 0), offset = Vector2(0, 0), zindex = zindex)

        self.change(tile_node = tile_node, one_tile_size = one_tile_size, zindex = zindex, active = True)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)

    def change(self, tile_node : resources.SpriteSheet = None, one_tile_size : Vector2 = None, zindex = None, active = None):
        if tile_node is not None:
            self.tile_node = tile_node

            for layer in self.children:
                if isinstance(layer, TileMapLayer):
                    for tile in layer.children:
                        if isinstance(tile, TileMapBlock):
                            tile.change(tile_node = self.tile_node)

        if one_tile_size is not None:
            try:
                old_size = self.tile_size.copy()
            except:
                old_size = Vector2(one_tile_size)
            self.tile_size = Vector2(one_tile_size)
            for layer in self.children:
                if isinstance(layer, TileMapLayer):
                    for tile in layer.children:
                        if isinstance(tile, TileMapBlock):
                            tile.change(size = self.tile_size, offset = Vector2(tile.offset.x / old_size.x * self.tile_size.x, tile.offset.y / old_size.y * self.tile_size.y))
                    
                    for collision_block in layer.collisionArea.collision_blocks:
                        collision_block.change(size = self.tile_size, offset = Vector2(tile.offset.x / old_size.x * self.tile_size.x, tile.offset.y / old_size.y * self.tile_size.y))

        super().nodeChange(zindex = zindex, active = active)
        
    def kill(self):
        super().kill()
    

    def addLayer(self, zindex = 0):
        return TileMapLayer(self, zindex)

class TileMapLayer(Node):
    def __init__(self, tileMap : TileMap, physical : bool = False, physics_layer : int = 0, zindex : float = 0):
        super().__init__(tileMap, size = Vector2(0, 0), offset = Vector2(0, 0), zindex = zindex)

        self.blocks = {}
        self.collision_blocks = {}

        self.collisionArea = CollisionArea(self, physics_layer = 0)
        self.change(physical = physical, physics_layer = physics_layer, zindex = zindex, active = True)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas : pygame.surface):
        canvas = super().draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        super().addChild(newChild)

    def change(self, physical : bool = None, physics_layer : int = None, zindex = None, active = None):
        if physical is not None:
            if physical:
                self.collisionArea.change(active = True)
            else:
                self.collisionArea.change(active = False)
        
        if physics_layer is not None:
            self.collisionArea.change(physics_layer = physics_layer)

        super().nodeChange(zindex = zindex, active = active)
        
    def kill(self):
        super().kill()
    

    def addTile(self, coords, tile_coords):
        self.blocks[tuple(coords)] = TileMapBlock(self, self.parentNode.tile_size, self.parentNode.tile_node, tile_coords, offset = Vector2(coords[0] * self.parentNode.tile_size[0], coords[1] * self.parentNode.tile_size[1]))
        
    
    def changeTile(self, coords, tile_coords):
        self.blocks[tuple(coords)].change(coords = tile_coords)
    
    def killTile(self, coords):
        if tuple(coords) in self.blocks:
            self.blocks[tuple(coords)].kill()
            del self.blocks[tuple(coords)]
    
    def addCollision(self, coords):
        self.collision_blocks[tuple(coords)] = CollisionBlock(self.collisionArea, self.parentNode.tile_size, offset = Vector2(coords[0] * self.parentNode.tile_size[0], coords[1] * self.parentNode.tile_size[1]))
        
    def killCollision(self, coords):
        if tuple(coords) in self.collision_blocks:
            self.collision_blocks[tuple(coords)].kill()
            del self.collision_blocks[tuple(coords)]






