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
        self.size = 720
        self.tiles = len(self.photos)

    def create(self, outfile):
        img = Image.new("RGB", (self.size, self.size), self.background)
        sizes = self.get_sizes()
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
        lines = math.floor(math.sqrt(self.tiles))
        SIZE = {}
        count = 1
        for x in range(lines):
            for y in range(lines):
                SIZE.update({count: {"size": [self.size / lines, self.size / lines],"where": [(self.size / lines) * x, (self.size / lines) * y]}})
                count += 1
        return SIZE

    def get_sizes_v2(self):
        lines = round(math.sqrt(self.tiles))
        baghi = self.tiles - (round(self.tiles / lines) * lines)
        SIZE = {}
        count = 1
        for x in range(lines):
            for y in range(lines):
                SIZE.update({count: {"size": [self.size / lines, self.size / lines],"where": [(self.size / lines) * x, (self.size / lines) * y]}})
                count += 1
        if baghi:
            for bag in range(baghi):
                ws = 1 if bag == 0 else bag
                SIZE.update({count: {"size": [self.size / ws, self.size / lines],"where": [(self.size / lines) * bag, (self.size / lines) * lines]}})
                count += 1
        return SIZE
