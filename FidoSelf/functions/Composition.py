from PIL import Image
import math

class Composition:
    def __init__(
        self,
        photos,
        background=(255, 255, 255),
    ):

        self.photos = photos
        self.background = background
        self.size = 1024
        self.tiles = len(self.photos)

    def create(self, outfile):
        img = Image.new("RGB", (self.size, self.size), self.background)
        sizes = self.get_sizes_v2()
        photos = self.photos[:len(sizes)]
        count = 1
        for photo in photos:
            image = Image.open(photo)
            size = (round(sizes[count]["size"][0]), round(sizes[count]["size"][1]))
            where = (round(sizes[count]["where"][0]), round(sizes[count]["where"][1]))
            newimage = image.resize(size)
            img.paste(newimage, where)
            count += 1
        img.save(outfile)
        return outfile
            
    def get_sizes(self):
        sqrt = math.sqrt(self.tiles)
        line = math.floor(sqrt)
        SIZE = {}
        count = 1
        for x in range(lines):
            for y in range(lines):
                SIZE.update({count: {"size": [self.size / line, self.size / line],"where": [(self.size / line) * x, (self.size / line) * y]}})
                count += 1
        return SIZE

    def get_sizes_v2(self):
        sqrt = math.sqrt(self.tiles)
        line = round(sqrt)
        all = line * line
        if all > self.tiles:
            all = line * (line - 1)
        other = self.tiles - all
        if other > 0:
            other += line
        SIZE = {}
        count = 1
        for x in range(line):
            for y in range(line):
                SIZE.update({count: {"size": [self.size / line, self.size / line],"where": [(self.size / line) * x, (self.size / line) * y]}})
                count += 1
        if other > 0:
            for i in range(other):
                SIZE.update({count: {"size": [self.size / other, self.size / line],"where": [(self.size / other) * i, (self.size / line) * (line - 1)]}})
                count += 1
        return SIZE
