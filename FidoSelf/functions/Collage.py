from PIL import Image
import os
import random

def make_collage(images, filename, width, init_height):
    margin_size = 2
    while True:
        images_list = images[:]
        coefs_lines = []
        images_line = []
        x = 0
        while images_list:
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            img.thumbnail((width, init_height))
            if x > width:
                coefs_lines.append((float(x) / width, images_line))
                images_line = []
                x = 0
            x += img.size[0] + margin_size
            images_line.append(img_path)
        coefs_lines.append((float(x) / width, images_line))

        if len(coefs_lines) <= 1:
            break
        if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):
            init_height -= 10
        else:
            break

    out_height = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            out_height += int(init_height / coef) + margin_size
    if not out_height:
        return False

    collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
    y = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            x = 0
            for img_path in imgs_line:
                img = Image.open(img_path)
                # if need to enlarge an image - use `resize`, otherwise use `thumbnail`, it's faster
                k = (init_height / coef) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                else:
                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
                if collage_image:
                    collage_image.paste(img, (int(x), int(y)))
                x += img.size[0] + margin_size
            y += int(init_height / coef) + margin_size
    collage_image.save(filename)
    return True
