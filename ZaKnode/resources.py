import os
import sys
import json
import pygame
from pygame import Vector2



# ----- Resources ----- #

## ----- Visual ----- ##


def directory(file, src : str):
    base_path = os.path.dirname(os.path.abspath(file))

    return os.path.normpath(os.path.join(base_path, src))

class Image:
    def __init__(self, path, alpha_channel = False):
        self.path = path
        self.rawImage = pygame.image.load(path)

        if alpha_channel:
            self.image = pygame.Surface(self.rawImage.get_size(), pygame.SRCALPHA)
        else:
            self.image = pygame.Surface(self.rawImage.get_size())

        self.image.blit(self.rawImage, Vector2(0, 0))

        self.rawImage = None

class SpriteSheet:
    def __init__(self, path, oneFrameSize, alpha_channel = False):
        self.path = path
        self.rawImage = pygame.image.load(path)

        self.grid = []
        self.tileCount = [self.rawImage.get_size()[0] // max(oneFrameSize[0], 1), self.rawImage.get_size()[1] // max(oneFrameSize[1], 1)]
        for x in range(int(self.tileCount[0])):
            self.grid.append([])
            for y in range(int(self.tileCount[1])):
                if alpha_channel:
                    oneTile = pygame.Surface(oneFrameSize, pygame.SRCALPHA)
                else:
                    oneTile = pygame.Surface(oneFrameSize)
                
                oneTile.blit(self.rawImage, Vector2(0, 0), 
                    (oneFrameSize[0] * x, oneFrameSize[1] * y, oneFrameSize[0], oneFrameSize[1]))
                self.grid[x].append(oneTile)
        
        self.rawImage = None

class Animation:
    def __init__(self, framesArr, start : int, end : int):
        if start > end:
            end, start = start, end

        self.frames = []
        for i in range(end - start + 1):
            frame = i + start
            x = frame % max(len(framesArr), 1)
            y = frame / max(len(framesArr), 1)
            self.frames.append(framesArr[int(x)][int(y)])

class Sound:
    def __init__(self, path, volume : float = 1):
        self.sound = pygame.mixer.Sound(path)
        self.volume = max(0, min(volume, 1))
        self.parent_volume = 1
        self.sound.set_volume(self.volume)
    
    def changeVolume(self, volume):
        self.volume = max(0, min(volume, 1))
        self.sound.set_volume(self.volume * self.parent_volume)


def SaveData(path, index, value):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            data[str(index)] = value

        with open(path, "w") as f:
            json.dump(data, f, indent = 4)
    except:
        with open(path, "w") as f:
            data = {}
            data[str(index)] = value
            json.dump(data, f, indent = 4)

def SaveDataList(path, index : list, value : list):
    if len(index) != len(value):
        print("number of indexes and values doesnt match")
        return "error"
    try:
        with open(path, "r") as f:
            data = json.load(f)
            for num in range(len(index)):
                data[str(index[num])] = value[num]

        with open(path, "w") as f:
            json.dump(data, f, indent = 4)
    except:
        with open(path, "w") as f:
            data = {}
            for num in range(len(index)):
                data[str(index[num])] = value[num]
            json.dump(data, f, indent = 4)

def ReadData(path, index = None):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            if index is not None:
                return data[str(index)]
            else:
                return data
    except:
        return None