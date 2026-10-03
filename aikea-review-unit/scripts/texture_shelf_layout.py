"""Scope: Place padded texture rectangles without rescaling their reserved texel widths."""

import math


class TextureShelfLayout:
    def __init__(self, size, padding=8, minimum=6):
        self.size = size
        self.padding = padding
        self.minimum = minimum

    def pack(self, spans, scale):
        rectangles = []
        for index, span in enumerate(spans):
            width, height = [max(self.minimum,math.ceil(value*scale)) for value in span]
            rectangles.append((index,width,height))
        rectangles.sort(key=lambda row:(-row[2],-row[1]))
        shelves = []
        placements = {}
        used_height = 0
        for index,width,height in rectangles:
            outer_width,outer_height = width+2*self.padding,height+2*self.padding
            if outer_width > self.size or outer_height > self.size:
                return None
            eligible = [shelf for shelf in shelves if shelf['height']>=outer_height
                        and shelf['x']+outer_width<=self.size]
            if eligible:
                shelf = min(eligible,key=lambda item:self.size-item['x']-outer_width)
            else:
                if used_height+outer_height > self.size:
                    return None
                shelf = {'x':0,'y':used_height,'height':outer_height}
                shelves.append(shelf)
                used_height += outer_height
            placements[index] = (shelf['x']+self.padding,shelf['y']+self.padding,width,height)
            shelf['x'] += outer_width
        return placements,used_height
