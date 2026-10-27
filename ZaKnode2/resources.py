import os
import sys
import json
import pygame
from pygame import Vector2



# ----- Resources ----- #

## ----- Visual ----- ##


def _directory(file, src : str):
    base_path = os.path.dirname(os.path.abspath(file))

    return os.path.normpath(os.path.join(base_path, src))

class Image:
    """
    Use Game.directory(relative path) in path for easier working with file paths
    Loads one image. pygame.Surface is in Image.image
    """
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
    """
    Use Game.directory(relative path) in path for easier working with file paths
    Loads image, cuts it into many smaller peaces and makes 2d array of tiles
    """
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
    """
    frames_arr takes a list of pygame.Surface objects
    ex.: [Image1.image, Image2.image] or [SpriteSheet1[0][1], SpriteSheet1[2][1]]
    Holds one animation, to be reused
    """
    def __init__(self, frames_arr, start : int, end : int):
        if start > end:
            end, start = start, end

        self.frames = []
        for i in range(end - start + 1):
            frame = i + start
            x = frame % max(len(frames_arr), 1)
            y = frame / max(len(frames_arr), 1)
            self.frames.append(frames_arr[int(x)][int(y)])

class Sound:
    """
    Volume is 0 - 100
    Loads sound/song file
    """
    def __init__(self, path, volume : int = 100):
        self.sound = pygame.mixer.Sound(path)
        self.volume = max(0, min(volume, 100))
        self.parent_volume = 100
        self.sound.set_volume(self.volume)
    
    def changeVolume(self, volume):
        self.volume = max(0, min(volume, 100))
        self.sound.set_volume((self.volume / 100) * (self.parent_volume / 100))


def SaveData(path, index, value):
    """
    Use Game.directory(relative path) in path for easier working with file paths
    Save data for next time, the game is run
    """
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
    """
    Use Game.directory(relative path) in path for easier working with file paths
    If saving multiple data points
    """
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
    """
    Use Game.directory(relative path) in path for easier working with file paths
    Reads the stored data
    """
    try:
        with open(path, "r") as f:
            data = json.load(f)
            if index is not None:
                return data[str(index)]
            else:
                return data
    except:
        return None