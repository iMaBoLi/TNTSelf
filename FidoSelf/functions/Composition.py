from PIL import Image
from math import floor

class Composition:
    def __init__(
        self,
        photos,
        background=(255, 255, 255),
    ):

        self.photos = photos
        self.background = background
        self.mode = "RGB"
        self.size = 500
        self.tiles = len(self.photos)

    def create(self, outfile):
        img = Image.new(self.mode, (self.size + 10, self.size + 10), self.background)
        sizes = self.get_sizes()
        count = 0
        for photo in self.photos:
            image = Image.open(photo)
            size = (round(sizes[count]["size"][0]), round(sizes[count]["size"][1]))
            where = (round(sizes[count]["where"][0]), round(sizes[count]["where"][1]))
            newimage = image.resize(size)
            img.paste(newimage, where)
            count += 1
        img.save(outfile)
        return outfile

    def get_sizes(self):
        rows = round(self.tiles / 2)
        lines = self.tiles - rows
        SIZE = {}
        for count in range(self.tiles):
            
            SIZE.update({count: {"size": [],"where": [,rows]}})
        return SIZE

        SIZES = {
            1: {
                1: {
                    "size": [self.size, rows],
                    "where": [0, 0],
                },
            },
            2: {
                1: {
                    "size": [self.size, rows],
                    "where": [0, 0],
                },
                2: {
                    "size": [self.size, rows],
                    "where": [0, self.size / 2],
                },
            },
            3: {
                1: {
                    "size": [self.size / 2, rows],
                    "where": [0, 0],
                },
                2: {
                    "size": [self.size / 2, rows],
                    "where": [self.size / 2, 0],
                },
                3: {
                    "size": [self.size, rows],
                    "where": [0, self.size / 2],
                },
            },
            4: {
                1: {
                    "size": [self.size / 2, rows],
                    "where": [0, 0],
                },
                2: {
                    "size": [self.size / 2, rows],
                    "where": [self.size / 2, 0],
                },
                3: {
                    "size": [self.size / 2, rows],
                    "where": [0, self.size / 2],
                },
                4: {
                    "size": [self.size / 2, rows],
                    "where": [self.size / 2, self.size / 2],
                },
            },
            5: {
                1: {
                    "size": [self.size / 3, rows],
                    "where": [0, 0],
                },
                2: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [self.size / 3, 0],
                },
                3: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [self.size / 3 * 2, 0],
                },
                4: {
                    "size": [self.size / 2, self.size / 2],
                    "where": [0, self.size / 2],
                },
                5: {
                    "size": [self.size / 2, self.size / 2],
                    "where": [self.size / 2, self.size / 2],
                },
            },
            6: {
                1: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [0, 0],
                },
                2: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [self.size / 3, 0],
                },
                3: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [self.size / 3 * 2, 0],
                },
                4: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [0, self.size / 2],
                },
                5: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [self.size / 3, self.size / 2],
                },
                6: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [self.size / 3 * 2, self.size / 2],
                },
            },
            7: {
                1: {
                    "size": [self.size / 4, self.size / 2],
                    "where": [0, 0],
                },
                2: {
                    "size": [self.size / 4, self.size / 2],
                    "where": [self.size / 4, 0],
                },
                3: {
                    "size": [self.size / 4, self.size / 2],
                    "where": [self.size / 4 * 2, 0],
                },
                4: {
                    "size": [self.size / 4, self.size / 2],
                    "where": [self.size / 4 * 3, 0],
                },
                5: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [0, self.size / 2],
                },
                6: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [self.size / 3, self.size / 2],
                },
                7: {
                    "size": [self.size / 3, self.size / 2],
                    "where": [self.size / 3 * 2, self.size / 2],
                },
            },
        }
        return SIZES[self.tiles]
