import math
import pygame
from pygame import Vector2

from .base import Modifier, Node


default_speed = 200

"""
class default(Modifier):
    def __init__(self, parentNode : Node):
        super().__init__(parentNode)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, active : bool = None):
        super().modifierChange(active = active)

    def kill(self):
        super().kill()
"""

def _avg(*args):
    return sum(args) / len(args)

def _getMousePosition(game, event = None):
    if event is not None:
        position_in_screen = Vector2(event.pos) - game.window.render_position
    else:
        position_in_screen = Vector2(pygame.mouse.get_pos()) - game.window.render_position

    return Vector2(int((game.simulation.size.x / game.window.render_size.x) * position_in_screen.x), int((game.simulation.size.y / game.window.render_size.y) * position_in_screen.y))

# ----------- Modifiers ------------ #

#   # -- Position changers -- ##

#       ## - Constant - ###


class AxisMove(Modifier):
    """
    Move an object on x/y axis
    """
    def __init__(self, parentNode : Node, start : int, end : int = None, axis : str = "x", mode : str = "linear", speed : float = default_speed, strength : float = 3, looping : bool = True, show_path : bool = False):
        super().__init__(parentNode)

        self.update_count = 0

        if end is None:
            axis_arr = {"x" : 0, "y" : 1}
            end = self.parentNode.offset[axis_arr.get(axis.lower(), 0)]
        
        self.elapsed = 0.0
        
        self.direction = 1

        self.change(start = start, end = end, axis = axis, mode = mode, speed = speed, strength = strength, looping = looping, show_path = show_path)

        self.last_offset = self.parentNode.offset[self.axis]


    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.duration == 0:
            return
        
        self.elapsed += self.direction * self.game.delta

        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.direction = -1
        elif self.elapsed <= 0:
            self.elapsed = 0
            self.direction = 1
        
        percents = self.elapsed / self.duration

        self.partition = self.mode(percents, self.strength)

        new_offset = self.start + self.path_len * self.partition

        changer = self.parentNode.offset

        changer[self.axis] += new_offset - self.last_offset
        
        self.parentNode.change(offset = changer)
        self.last_offset = new_offset

        if self.direction == -1 and not self.looping:
            self.kill()

        super().update()

    def draw(self, canvas):
        if self.show:
            pass
        canvas = super().draw(canvas)

        return canvas

    def change(self, start : int = None, end : int = None, axis : str = None, mode : str = None, speed : float = None, strength : float = None, looping : bool = None, show_path : bool = None, active : bool = None):
        if show_path is not None:
            self.show = show_path
        
        if looping is not None:
            self.looping = looping

        if axis is not None:
            axis_arr = {"x" : 0, "y" : 1}
            self.axis = axis_arr.get(axis.lower(), 0)
        
        if end is not None:
            self.end = end
        
        if start is not None:
            self.start = start
        
        if self.start > self.end:
            self.start, self.end = self.end, self.start
        
        if speed is not None:
            self.speed = speed

        if strength is not None:
            self.strength = abs(strength)

        if start is not None or end is not None or speed is not None or axis is not None:
            if self.parentNode.offset[self.axis] < self.start:
                self.parentNode.change(offset = self.start)
            elif self.parentNode.offset[self.axis] > self.end:
                self.parentNode.change(offset = self.end)

            self.path_len = self.end - self.start
            self.duration = self.path_len / self.speed if self.speed != 0 else 0

        if mode is not None:
            modes = {
                "linear" : self._linear,
                "ease-in" : self._easeIn,
                "ease-out" : self._easeOut,
                "ease-both" : self._easeBoth,
                "ease-in-out" : self._easeBoth
            }

            self.mode = modes.get(mode, self._linear)

        super().modifierChange(active)

    def kill(self):
        super().kill()
    
    
    def _linear(self, p, s):
        return p

    def _easeIn(self, p, s):
        return pow(p, s)
    
    def _easeOut(self, p, s):
        return 1 - pow(1 - p, s)
    
    def _easeBoth(self, p, s):
        if p < 0.5:
            return pow(2, s - 1) * pow(p, s)
        else:
            return 1 - pow(-2 * p + 2, s) / 2

class LinearMove(Modifier):
    """
    Move an object from one point to another and back 
    """
    def __init__(self, parentNode : Node, end : Vector2, start : Vector2 = None, mode : str = "linear", speed : float = default_speed, strength : float = 3, looping : bool = True, show_path : bool = False):
        super().__init__(parentNode)

        if start is None:
            start = self.parentNode.offset

        self.elapsed = 0.0

        self.direction = 1

        self.change(end = end, start = start, mode = mode, speed = speed, strength = strength, looping = looping, show_path = show_path)

        self.last_offset = Vector2(0, 0)


    
    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.duration == 0:
            return
        
        self.elapsed += self.direction * self.game.delta

        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.direction = -1
        elif self.elapsed <= 0:
            self.elapsed = 0
            self.direction = 1
        
        percents = self.elapsed / self.duration

        self.partition = self.mode(percents, self.strength)

        self.new_offset = self.difference * self.partition

        step = self.new_offset - self.last_offset
        
        self.parentNode.change(offset = self.parentNode.offset + step)
        self.last_offset = self.new_offset

        if self.direction == -1 and not self.looping:
            self.kill()

        super().update()

    def draw(self, canvas):
        if self.show:
            pass
        canvas = super().draw(canvas)

        return canvas
    
    def change(self, end : Vector2 = None, start : Vector2 = None, mode : str = None, speed : int = None, strength : float = None, looping : bool = None, show_path : bool = None, active : bool = None):
        
        if looping is not None:
            self.looping = looping
        
        if show_path is not None:
            self.show = show_path
        
        if speed is not None:
            self.speed = abs(speed)
        
        if strength is not None:
            self.strength = abs(strength)

        if end is not None:
            self.end = Vector2(end)
        
        if start is not None:
            self.start = Vector2(start)

        if start is not None or end is not None:
            self.difference = self.end - self.start
            self.path_len = self.difference.length()

        self.duration = self.path_len / self.speed if self.speed != 0 else 0
        
        if mode is not None:
            modes = {
                "linear" : self.linear,
                "ease-in" : self.easeIn,
                "ease-out" : self.easeOut,
                "ease-both" : self.easeBoth,
                "ease-in-out" : self.easeBoth
            }

            self.mode = modes.get(mode, self.linear)
        
        if start is not None:
            self.parentNode.change(offset = self.start)
        
        super().modifierChange(active)

    def kill(self):
        super().kill()
    
    
    def linear(self, p, s):
        return p

    def easeIn(self, p, s):
        return pow(p, s)
    
    def easeOut(self, p, s):
        return 1 - pow(1 - p, s)
    
    def easeBoth(self, p, s):
        if p < 0.5:
            return pow(2, s - 1) * pow(p, s)
        else:
            return 1 - pow(-2 * p + 2, s) / 2

class CircularMove(Modifier):
    """
    Moves an object in a circular motion
    """
    def __init__(self, parentNode : Node, relative_center : Vector2, radius : float = None, clockwise : bool = True, start_deg : float = 0, speed : float = default_speed, show_path : bool = False):
        super().__init__(parentNode)

        self.change(relative_center = relative_center, radius = radius, clockwise = clockwise, start_deg = start_deg, speed = speed, show_path = show_path)
        
        self.last_offset = self.parentNode.offset
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.duration == 0:
            return

        self.elapsed += self.game.delta * self.direction

        if self.elapsed >= self.duration or self.elapsed <= 0:
            self.elapsed = self.elapsed % self.duration
        
        percents = self.elapsed / self.duration

        self.angle = 2 * math.pi * percents

        self.new_offset = Vector2(self.center.x + math.cos(self.angle) * self.radius, self.center.y + math.sin(self.angle) * self.radius)


        step = self.new_offset - self.last_offset
        
        self.parentNode.change(offset = self.parentNode.offset + step)

        self.last_offset = self.new_offset

        super().update()

    def draw(self, canvas):
        if self.show:
            center = self.parentNode.position + Vector2(math.cos(self.angle) * self.radius, math.sin(self.angle) * self.radius) * -1
            pygame.draw.circle(canvas, (255, 0, 0), center, abs(self.radius), width = 2)
        canvas = super().draw(canvas)

        return canvas

    def kill(self):
        super().kill()
    

    def change(self, relative_center : Vector2 = None, radius : float = None, clockwise : bool = None, start_deg : float = None, speed : float = None, show_path : bool = None, active : bool = None):

        if relative_center is not None:
            self.center = self.parentNode.offset + Vector2(relative_center)
            if radius is None:
                difference = self.parentNode.offset - self.center
                self.radius = difference.length()
            else:
                self.radius = radius
            self.path_len = 2 * math.pi * self.radius
        else:
            if radius is not None:
                self.radius = radius
                self.path_len = 2 * math.pi * self.radius
        
        if show_path is not None:
            self.show = show_path

        if speed is not None:
            self.speed = max(speed, 0)

        if clockwise is not None:
            self.direction = 1 if clockwise else -1

        if start_deg is None:
            start_deg = (self.angle / (2 * math.pi)) * 360
        self.angle = math.radians(start_deg)

        
        self.duration = self.path_len / self.speed if self.speed != 0 else 0

        self.elapsed = (start_deg / 360) * self.duration


        super().modifierChange(active)


class Follow(Modifier):
    """
    Makes an object follow anothers object origin
    """
    def __init__(self, parentNode : Node, follow_node : Node, axis : str = "both", speed : float = default_speed):
        super().__init__(parentNode)
        self.change(follow_node = follow_node, speed = speed, axis = axis)

    def event(self, event):
        super().event(event)
    
    def update(self):
        direction = self.follow_node.position - self.parentNode.position 
        if direction != Vector2(0, 0):
            changer = self.parentNode.offset
            step = self.speed * self.game.delta * direction.normalize()
            for i in self.axis:
                changer[i] += step[i]
            if step.length() > direction.length():
                for i in self.axis:
                    changer[i] = (self.follow_node.position - self.parentNode.parentNode.position)[i]
            self.parentNode.change(offset = changer)
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, follow_node : Node = None, speed : int = None, axis : str = None, active : bool = None):
        if follow_node is  not None:
            self.follow_node = follow_node

        if speed is not None:
            self.speed = speed

        if axis is not None:
            axis_arr = {"x" : [0], "y" : [1], "both" : [0, 1], "all" : [0, 1]}
            self.axis = axis_arr.get(axis.lower(), [0, 1])
            
        super().modifierChange(active)

    def kill(self):
        super().kill()


class Centralize(Modifier):
    """
    IDK if works well
    Puts an objects origin into the center of "camera"
    """
    def __init__(self, parentNode : Node, scene : Node):
        super().__init__(parentNode, zindex = 100)
        self.scene = scene

    def event(self, event):
        super().event(event)
    
    def update(self):
        self.scene.change(offset = self.game.size / 2 - (self.parentNode.position - self.scene.position))
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, active : bool = None):
        super().modifierChange(active)

    def kill(self):
        self.scene.change(offset = Vector2(0, 0))
        super().kill()
        

#       ## - Mouse - ###

class MouseClickMove(Modifier):
    """
    Object moves to position, where mouse clicks at
    """
    def __init__(self, parentNode : Node):
        super().__init__(parentNode)
    

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = _getMousePosition(self.game, event)
            self.parentNode.change(offset = mouse - self.parentNode.parentNode.position + self.game.scenes.scenes[self.game.scenes.current_scene].position)
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, active : bool = None):
        super().modifierChange(active)

    def kill(self):
        super().kill()

class MouseDragMove(Modifier):
    """
    Physics layers are taken in base 2 (1, 2, 4, 8, 16, etc.) (you can do combinations)
    Drag an object by mouse
    """
    def __init__(self, parentNode : Node, physics_check : int = 1, axis : str = None):
        super().__init__(parentNode)

        self.axis = [0, 1]
        
        self.mouse_offset = Vector2(0, 0)

        self.change(physics_check = physics_check, axis = axis)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mouse = _getMousePosition(self.game, event)

            for collision_area in self.parentNode.collision:
                if collision_area.physics_layer == self.physics_check:
                    for rect in collision_area.collision_blocks:
                        if rect.rect.collidepoint(mouse):
                            self.mouse_offset = self.parentNode.position - mouse
                            self.mouse_clicked = True
                            return
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouse_clicked = False
        super().event(event)
    
    def update(self):
        if self.mouse_clicked:

            mouse = _getMousePosition(self.game)

            global_pos = mouse + self.mouse_offset
            new_offset = self.parentNode.offset
            for i in self.axis:
                new_offset[i] = global_pos[i] - self.parentNode.parentNode.position[i]
            self.parentNode.change(offset = new_offset)

        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas
    
    def change(self, physics_check = None, axis = None, active = None):
        axis_arr = {"x" : [0], "y" : [1], "all" : [0, 1], "both" : [0, 1], "xy" : [0, 1]}

        if axis is not None:
            self.axis = axis_arr.get(axis.lower(), [0, 1])

        if physics_check is not None:
            self.physics_check = physics_check
            self.mouse_clicked = False

        super().modifierChange(active)

    def kill(self):
        super().kill()


#       ## - Keyboard - ###

class _KeyboardMove(Modifier):
    def __init__(self, parentNode, speed, leave_window):
        super().__init__(parentNode)

        self.change(speed = speed, leave_window = leave_window)


    def event(self, event):
        super().event(event)
    
    def update(self, direction):
        if direction.length_squared() > 0:
            direction = direction.normalize()

        step = self.parentNode.offset + direction * self.speed * self.game.delta
        self.parentNode.change(offset = step)

        if not self.leave_window:
            max_x = self.game.size[0] - self.parentNode.size.x
            max_y = self.game.size[1] - self.parentNode.size.y

            self.parentNode.change(offset = Vector2(max(0, min(max_x, self.parentNode.offset.x)), max(0, min(max_y, self.parentNode.offset.y))))

        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, speed : float = None, leave_window : bool = None, active : bool = None):
        if speed is not None:
            self.speed = speed
        
        if leave_window is not None:
            self.leave_window = leave_window

        super().modifierChange(active)

    def kill(self):
        super().kill()

class KeyboardArrowsMove(_KeyboardMove):
    """
    Move an object by arrows
    """
    def __init__(self, parentNode : Node, speed : float = default_speed, leave_window : bool = False):
        super().__init__(parentNode, speed = speed, leave_window = leave_window)


    def event(self, event):
        super().event(event)
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        direction = Vector2(0, 0)
        direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        super().update(direction)

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas
    
    def change(self, speed : float = None, leave_window : bool = None,  active : bool = None):
        super().change(speed = speed, leave_window = leave_window, active = active)

    def kill(self):
        super().kill()

class KeyboardWASDMove(_KeyboardMove):
    """
    Move an object by WASD
    """
    def __init__(self, parentNode : Node, speed : float = default_speed, leave_window : bool = False):
        super().__init__(parentNode, speed = speed, leave_window = leave_window)


    def event(self, event):
        super().event(event)
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        direction = Vector2(0, 0)
        direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        direction.y = keys[pygame.K_s] - keys[pygame.K_w]

        super().update(direction)

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas
    
    def change(self, speed : float = None, leave_window : bool = None, active : bool = None):
        super().change(speed = speed, leave_window = leave_window, active = active)

    def kill(self):
        super().kill()
    

#   # -- User func -- ##

class ClickObject(Modifier):
    """
    Physics layers are taken in base 2 (1, 2, 4, 8, 16, etc.) (you can do combinations)
    Button intigers (none - all, 1 - left, 2 - middle, 3 - right)
    Function will run when hitbox is clicked on/released on with any/one button 
    """
    def __init__(self, parentNode : Node, physics_check : int, function : callable, buttondown : bool = True, button : int = None):
        super().__init__(parentNode)
        
        self.func = function
        self.button = button
        
        self.physics_check = physics_check

        if buttondown:
            self.event_type = pygame.MOUSEBUTTONDOWN
        else:
            self.event_type = pygame.MOUSEBUTTONUP

    def event(self, event):
        if event.type == self.event_type and self._pressed(event):

            mouse = _getMousePosition(self.game, event)

            for collision_area in self.parentNode.collision:
                if not collision_area.active:
                    continue

                if collision_area.physics_layer & self.physics_check == 0:
                    continue

                for rect in collision_area.collision_blocks:
                    if not rect.active:
                        continue
                    if rect.rect.collidepoint(mouse):
                        self.func()
                        return

        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, physics_check : int = None, func = None, buttondown : bool = None, button : int = None, active : bool = None):
        if physics_check is not None:
            self.physics_check = physics_check

        if func is not None:
            self.func = func
        
        if buttondown is not None:
            if buttondown:
                self.event_type = pygame.MOUSEBUTTONDOWN
            else:
                self.event_type = pygame.MOUSEBUTTONUP

        if button is not None:
            self.button = button
        
        super().modifierChange(active)

    def kill(self):
        super().kill()
    

    def _pressed(self, event):
        if self.button is None:
            return True
        return event.button == self.button

class HoldObject(Modifier):
    """
    Physics layers are taken in base 2 (1, 2, 4, 8, 16, etc.) (you can do combinations)
    Runs the function while pressing any/selected mouse button/s
    Runs else_func function, if the opposit (not holding)
    """
    def __init__(self, parentNode : Node, physics_check : int, function : callable, button : int = None, else_function : callable = None):
        super().__init__(parentNode)

        self.else_func = None
        self.button = None
        self.change(physics_check, function, button, else_function)

        self.holding = False

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.pressed(event):

            mouse = _getMousePosition(self.game, event)

            for collision_area in self.parentNode.collision:
                if not collision_area.active:
                    continue

                if collision_area.physics_layer & self.physics_check == 0:
                    continue

                for rect in collision_area.collision_blocks:
                    if rect.rect.collidepoint(mouse):
                        self.holding = True
                        break

                if self.holding:
                    break
    
        elif event.type == pygame.MOUSEBUTTONUP and self._pressed(event):
            self.holding = False

        super().event(event)
    
    def update(self):
        if self.holding:
            self.func()
        else:
            if self.else_func is not None:
                self.else_func()
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas
    
    def change(self, physics_check : int = None, func : callable = None, button : int = None, else_func : callable = None, active : bool = None):
        if physics_check is not None:
            self.physics_check = physics_check
        
        if func is not None:
            self.func = func
        
        if button is not None:
            self.button = button
        
        if else_func is not None:
            self.else_func = else_func

        super().modifierChange(active)

    def kill(self):
        super().kill()
    

    def _pressed(self, event):
        if self.button is None:
            return True
        return event.button == self.button
    
class Hover(Modifier):
    """
    Physics layers are taken in base 2 (1, 2, 4, 8, 16, etc.) (you can do combinations)
    If hovering over hitbox with mouse, function will be run once.
    After leaving, it will run else_func function (if set).
    """
    def __init__(self, parentNode : Node, physics_check : int, func : callable, else_func : callable = None):
        super().__init__(parentNode)
        self.last_frame = False
        self.else_func = None
        self.change(physics_check = physics_check, func = func, else_func = else_func)

    def event(self, event):     
        super().event(event)
    
    def update(self):
        did = False

        mouse = _getMousePosition(self.game)

        for collision_area in self.parentNode.collision:
            if not collision_area.active:
                continue
            if collision_area.physics_layer & self.physics_check == 0:
                continue
            for rect in collision_area.collision_blocks:
                if rect.rect.collidepoint(mouse):
                    self.func()
                    did = True
        
        if not did and self.last_frame and self.else_func is not None:
            self.else_func()
        
        self.last_frame = did
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas
    
    def change(self, physics_check = None, func = None, else_func = None, active : bool = None):
        if physics_check is not None:
            self.physics_check = physics_check
        
        if func is not None:
            self.func = func
        
        if else_func is not None:
            self.else_func = else_func

        super().modifierChange(active)

    def kill(self):
        super().kill()

class PressKey(Modifier):
    """
    Key is int for mouse (none - all, 1 - left, 2 - middle, 3 - right)
    Key is pygame.K_... (from pygame)
    Function will run once after pressing or releasing a key or a button (all is settible)
    """
    def __init__(self, parentNode : Node, key, function : callable, keydown : bool = True, mouse : bool = False):
        super().__init__(parentNode)

        self.mouse_press = False
        
        self.change(key = key, func = function, keydown = keydown, mouse = mouse, active = True)

    def event(self, event):
        if event.type == self.event_type and self.input_type(event):
            self.func()

        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas
    
    def change(self, key = None, func : callable = None, keydown : bool = None, mouse : bool = None, active : bool = None):
        if key is not None:
            self.key = key
        
        if func is not None:
            self.func = func

        if keydown is not None:
            self.keydown = keydown

        if mouse is not None:
            self.mouse_press = mouse
        
        if mouse is not None or keydown is not None:
            if self.mouse_press:
                self.input_type = self._mouse
                if self.keydown:
                    self.event_type = pygame.MOUSEBUTTONDOWN
                else:
                    self.event_type = pygame.MOUSEBUTTONUP
            else:
                self.input_type = self._keyboard
                if self.keydown:
                    self.event_type = pygame.KEYDOWN
                else:
                    self.event_type = pygame.KEYUP

        super().modifierChange(active)

    def kill(self):
        super().kill()
    

    def _mouse(self, event):
        return event.button == self.key
    
    def _keyboard(self, event):
        return event.key == self.key

class HoldKey(Modifier):
    """
    Key is int for mouse (none - all, 1 - left, 2 - middle, 3 - right)
    Key is pygame.K_... (from pygame)
    Function will run any time and while you press a key or button
    """
    def __init__(self, parentNode : Node, key, function : callable, mouse : bool = False):
        super().__init__(parentNode)

        self.holding = False
        self.change(key = key, func = function, mouse = mouse)

    def event(self, event):
        if event.type == self.event_type and self.input_type(event):
            self.holding = True
        elif event.type == self.else_event_type and self.input_type(event):
            self.holding = False

        super().event(event)
    
    def update(self):
        if self.holding:
            self.func()
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas
    
    def change(self, key = None, func : callable = None, keydown : bool = None, mouse : bool = None, active : bool = None):
        if key is not None:
            self.key = key
        
        if func is not None:
            self.func = func

        if mouse is not None:
            self.mouse_press = mouse
        
        if mouse is not None or keydown is not None:
            if self.mouse_press:
                self.input_type = self._mouse
                self.event_type = pygame.MOUSEBUTTONDOWN
                self.else_event_type = pygame.MOUSEBUTTONUP
            else:
                self.input_type = self._keyboard
                self.event_type = pygame.KEYDOWN
                self.else_event_type = pygame.KEYUP

        super().modifierChange(active)

    def kill(self):
        super().kill()
    

    def _mouse(self, event):
        return event.button == self.key
    
    def _keyboard(self, event):
        return event.key == self.key

class OnEventFunc(Modifier):
    """
    Will pass pygame event, if there is any
    """
    def __init__(self, parentNode : Node, func : callable):
        super().__init__(parentNode)
        self.change(func = func)

    def event(self, event):
        self.func(event)
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, func : callable = None, active : bool = None):
        if func is not None:
            self.func = func

        super().modifierChange(active)

    def kill(self):
        super().kill()

class ForeverDo(Modifier):
    """
    Function will run every frame, if object is active
    """
    def __init__(self, parentNode : Node, func : callable):
        super().__init__(parentNode)
        self.change(func = func)

    def event(self, event):
        super().event(event)
    
    def update(self):
        self.func()
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, func : callable = None, active : bool = None):
        if func is not None:
            self.func = func
        super().modifierChange(active)

    def kill(self):
        super().kill()

class SignalTrigger(Modifier):
    """
    Uses single use trigger, made in Game object
    """
    def __init__(self, parentNode : Node, signal_name : str, func : callable):
        super().__init__(parentNode)

        self.change(name = signal_name, func = func)

    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.game.signals.signals[self.signal_name]:
            self.game.signals.signals[self.signal_name] = False
            self.func()
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, name : str = None, func : callable = None, active : bool = None):
        if name is not None:
            self.signal_name = name
        if func is not None:
            self.func = func
        super().modifierChange(active)

    def kill(self):
        super().kill()

class OnCollideDo(Modifier):
    """
    Physics layers are taken in base 2 (1, 2, 4, 8, 16, etc.) (you can do combinations)
    Run function while 2 areas are colliding
    """
    def __init__(self, parentNode : Node, func : callable, physics_check : int, parent_physics_layer : int = None):
        super().__init__(parentNode)
        if parent_physics_layer is None:
            parent_physics_layer = "all"

        self.change(func = func, physics_check = physics_check, parent_physics_layer =  parent_physics_layer)

    def event(self, event):
        super().event(event)
    
    def update(self):
        self_collisions = []
        
        for parentColArea in self.parentNode.collision:
            if not parentColArea.active:
                continue

            if not self.parent_physics_check(parentColArea):
                continue

            for parentRect in parentColArea.collision_blocks:
                if not parentRect.active:
                    self_collisions.append(parentRect.rect)

        if self._checkForCollision(self.game.scenes.scenes[self.game.scenes.current_scene], self_collisions):
            self.func()

        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, func : callable = None, physics_check : int = None, parent_physics_layer : int = None, active : bool = None):
        if func is not None:
            self.func = func

        if physics_check is not None:
            self.physics_check = physics_check

        if parent_physics_layer is not None:
            if parent_physics_layer == "all":
                self.parent_physics_check = self._allParentLayers
            else:
                self.parent_physics_check = self._parentLayers
                self.parent_physics = list(parent_physics_layer)

        super().modifierChange(active)

    def kill(self):
        super().kill()

    
    def _allParentLayers(self, collision_area):
        return True
    
    def _parentLayers(self, collision_area):
        return collision_area.physics_layer in self.parent_physics

    def _checkForCollision(self, parentNode, self_collisions):
        if not parentNode.active:
            return False
        
        for node in parentNode.children:
            if not node.active:
                continue

            if hasattr(node, "collision"):
                for collisionArea in node.collision:
                    if not collisionArea.active:
                        continue

                    if collisionArea.physics_layer & self.physics_check == 0:
                        continue

                    for collision_block in collisionArea.collision_blocks:
                        if not collision_block.active:
                            continue

                        if collision_block.rect.collidelist(self_collisions) != -1:
                            return True
                                
            if hasattr(node, "children"):
                if self._checkForCollision(node, self_collisions):
                    return True
            
        return False

class OnCollideBothObjects(Modifier):
    """
    Physics layers are taken in base 2 (1, 2, 4, 8, 16, etc.) (you can do combinations)
    Single atribute of your function must be an ZaKnode object, the object, the other collision area is on.
    It will never be able to affect multiple objects, on it's own.
    """
    def __init__(self, parentNode : Node, func : callable, physics_check : int, parent_physics_layer : int = None):
        super().__init__(parentNode)
        if parent_physics_layer is None:
            parent_physics_layer = "all"
            
        self.change(func = func, physics_check = physics_check, parent_physics_layer =  parent_physics_layer)

    def event(self, event):
        super().event(event)
    
    def update(self):
        self_collisions = []
        
        for parentColArea in self.parentNode.collision:
            if not parentColArea.active:
                continue

            if not self.parent_physics_check(parentColArea):
                continue

            for parentRect in parentColArea.collision_blocks:
                if not parentRect.active:
                    self_collisions.append(parentRect.rect)

        output = self._checkForCollision(self.game.scenes.scenes[self.game.scenes.current_scene], self_collisions)
        if output[0]:
            self.func(output[1])

        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, func : callable = None, physics_check : int = None, parent_physics_layer : int = None, active : bool = None):
        if func is not None:
            self.func = func

        if physics_check is not None:
            self.physics_check = physics_check

        if parent_physics_layer is not None:
            if parent_physics_layer == "all":
                self.parent_physics_check = self._allParentLayers
            else:
                self.parent_physics_check = self._parentLayers
                self.parent_physics = list(parent_physics_layer)

        super().modifierChange(active)

    def kill(self):
        super().kill()

    
    def _allParentLayers(self, collision_area):
        return True
    
    def _parentLayers(self, collision_area):
        return collision_area.physics_layer in self.parent_physics

    def _checkForCollision(self, parentNode, self_collisions):
        if not parentNode.active:
            return [False, None]
        
        if not hasattr(parentNode, "children"):
            return [False, None]
        
        for node in parentNode.children:
            if not node.active:
                continue

            if not hasattr(node, "collision"):
                continue

            for collision_area in node.collision:
                if not collision_area.active:
                    continue

                if collision_area.physics_layer != self.physics_check:
                    continue

                for collision_block in collision_area.collision_blocks:
                    if not collision_block.active:
                        continue

                    if collision_block.rect.collidelist(self_collisions) != -1:
                        return [True, node]
                                    
            if hasattr(node, "children"):
                found, collisionParent =  self._checkForCollision(node, self_collisions)
                if found:
                    return [True, collisionParent]

        return [False, None]

class Timer(Modifier):
    """
    Start timer, to delay function by x seconds
    """
    def __init__(self, parentNode : Node, time : float, func : callable):
        super().__init__(parentNode)
        self.elapsed = 0.0
        self.active = False
        self.change(time = time, func = func)

    def event(self, event):
        super().event(event)
    
    def update(self):
        if self.active:
            self.elapsed += self.game.delta
            if self.elapsed >= self.time:
                self.func()
                self.end()
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, time : float = None, func : callable = None, active : bool = None):
        if time is not None:
            self.time = time
        
        if func is not None:
            self.func = func
        super().modifierChange(active)

    def kill(self):
        super().kill()

    
    def start(self):
        self.elapsed = 0.0
        self.active = True
    
    def pause(self):
        self.active = self.active == False
    
    def end(self):
        self.active = False



#   # -- Sound/Music -- ##

class _GlobalAPlayer(Modifier):
    def __init__(self, parentNode : Node, volume : int = 100):
            super().__init__(parentNode)
            self.sounds = {}
    
            self.change(volume = volume)
    
    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)

        return canvas

    def change(self, volume : int = None, active : bool = None):
        if volume is not None:
            self.volume = max(0, min(volume, 100))
            for sound in self.sounds.values():
                sound.parent_volume = self.volume
                sound.sound.set_volume((sound.volume / 100) * (self.volume / 100))
        super().modifierChange(active)

    def kill(self):
        super().kill()

    def add(self, name : str, sound):
        self.sounds[name] = sound

    def play(self, name : str):
        self.sounds[name].sound.play()

    def stop(self, name : str):
        self.sounds[name].sound.stop()


class GlobalSoundEffectPlayer(_GlobalAPlayer):
    """
    Play sounds - one shoot audio
    """
    def __init__(self, parentNode : Node, volume : int = 100):
        super().__init__(parentNode, volume)

    def event(self, event):
        super().event(event)
    
    def update(self):
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)
        return canvas

    def change(self, volume : int = None, active : bool = None):
        super().change(volume, active)

    def kill(self):
        super().kill()

    def add(self, name : str, sound):
        super().add(name, sound)
    
    def play(self, name : str):
        super().play(name)

    def stop(self, name : str):
        super().stop(name)

class GlobalMusicPlayer(_GlobalAPlayer):
    """
    Play music - looping
    """
    def __init__(self, parentNode : Node, volume : int = 100):
        super().__init__(parentNode, volume)
        self.queue = {}
        self.playing = []

    def event(self, event):
        super().event(event)
    
    def update(self):
        for song in self.sounds.keys():
            if self.sounds[song].get_busy():
                if not song in self.playing:
                    self.playing.append(song)
            else:
                if song in self.playing:
                    self.playing.remove(song)
        super().update()

    def draw(self, canvas):
        canvas = super().draw(canvas)
        return canvas

    def change(self, volume : int = None, active : bool = None):
        super().change(volume, active)

    def kill(self):
        super().kill()


    def add(self, name : str, sound):
        super().add(name, sound)
    
    def playLooping(self, name : str):
        self.sounds[name].sound.play(loops = -1)

    def play(self, name : str):
        super().play(name)

    def playAfter(self, afterThis : str, name : str):
        self.queue[afterThis] = name

    def pause(self, name : str):
        if self.sounds[name].get_busy():
            self.sounds[name].pause()
        else:
            self.sounds[name].unpause()

    def stop(self, name : str):
        super().stop(name)

