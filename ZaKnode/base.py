import math
import pygame
from pygame import Vector2


__all__ = ["Modifier", "Node"]


def positionFromStr(string: str, size, parentNode_size):
    sw, sh = Vector2(size)
    pw, ph = Vector2(parentNode_size)
    
    max_x, max_y = pw - sw, ph - sh
    mid_x, mid_y = max_x / 2, max_y / 2

    pos = {
        "top-left":     Vector2(0, 0),
        "left":         Vector2(0, mid_y),
        "bottom-left":  Vector2(0, max_y),
        "top-right":    Vector2(max_x, 0),
        "right":        Vector2(max_x, mid_y),
        "bottom-right": Vector2(max_x, max_y),
        "top":          Vector2(mid_x, 0),
        "bottom":       Vector2(mid_x, max_y),
        "center":       Vector2(mid_x, mid_y)
    }

    output = pos.get(string, Vector2(0, 0))
    
    return Vector2(output)


# ----- Base of nodes ----- #


class Base:
    def __init__(self, parentNode, zindex : int = 0, active : bool = True):
        self.zindex = zindex

        self.parentNode = parentNode
        self.parentNode.addChild(self)

        self.game = self.parentNode.game

        self.universalChange(active)


    def kill(self):
        if hasattr(self, "children"):
            for child in self.children[:]:
                child.kill()

            self.children.clear()
            self.collision.clear()

        if self.parentNode:
            if self in self.parentNode.children:
                self.parentNode.children.remove(self)
            self.parentNode = None
    
    def universalChange(self, active = None):
        if active is not None:
            self.active = active


class Modifier(Base):
    def __init__(self, parentNode, zindex : int = -10, active : bool = True):
        super().__init__(parentNode, zindex, active)
    
    def event(self, event):
        pass
    
    def update(self):
        pass

    def draw(self, canvas : pygame.surface):
        return canvas
    
    def kill(self) -> None:
        super().kill()
    
    def modifierChange(self, active : bool = None):
        super().universalChange(active)
        

class Node(Base):
    def __init__(self, parentNode, size : Vector2 = Vector2(0, 0), offset_str : str = None, offset : Vector2 = Vector2(0, 0), zindex : int = 0, active : bool = True):
        super().__init__(parentNode, zindex = zindex, active = active)
        self.children = []
        self.collision = []

        self.nodeChange(size = size, offset_str = offset_str, offset = offset, zindex = zindex)

    def event(self, event):
        for node in self.children:
            if node.active:
                node.event(event)
    
    def update(self):
        for node in self.children:
            if node.active:
                node.update()

    def draw(self, canvas : pygame.surface):
        for node in self.children:
            if node.active:
                canvas = node.draw(canvas)

        return canvas
    
    def addChild(self, newChild):
        for i in range(len(self.children)):
            if self.children[i].zindex >= newChild.zindex:
                self.children.insert(i, newChild)
                return
        self.children.append(newChild)
    
    def addCollision(self, newCollision):
        self.collision.append(newCollision)

    def nodeChange(self, size = None, offset_str = None, offset = None, zindex = None, active = None):
        if size is not None:
            self.size = Vector2(size)

        if zindex is not None:
            self.zindex = zindex
            self.parentNode.children.remove(self)
            self.parentNode.addChild(self)

        if offset_str is not None:
            self.offset = positionFromStr(offset_str.lower(), self.size, self.parentNode.size)
            if offset is not None:
                self.offset += Vector2(offset)
        elif offset is not None:
            self.offset = Vector2(offset)
        
        self.position = self.parentNode.position + self.offset

        super().universalChange(active)

        for child in self.children:
            child.change()
    
    def kill(self):
        super().kill()

