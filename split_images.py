import argparse

from os import scandir, mkdir

import numpy as np

from PIL import Image


def load_image(_path:str):

    files = sorted([f.path for f in scandir(_path) if f.is_file()])

    images = []
    borders = []
    avg_left = []
    avg_right = []

    for file in files:
        print(f"{file}")
        fp = open(file, 'rb')
        img = Image.open(fp)

        l_b, r_b = find_borders(img)
        h = img.height
        cropped_width = r_b - l_b

        if should_split(cropped_width, h):
            avg_left.append(l_b)
            avg_right.append(r_b)

        borders.append((l_b, r_b))
        images.append([img])
        fp.close()

    left_border = sorted(avg_left)[(len(avg_left)+1) // 2]
    right_border = sorted(avg_right)[(len(avg_right)+1) // 2]

    for i, border in enumerate(borders):
        l_b, r_b = border
        h = images[i][0].height
        cropped_width = r_b - l_b

        if should_split(cropped_width, h):
            mid = (right_border - left_border) // 2 + left_border
            images[i] += [(mid+1, 0, right_border, h), (left_border, 0, mid, h)]
        else:
            images[i] += [(l_b, 0, r_b, h)]

    batch_save(_path, images)

def batch_save(_path:str, images: list) -> None:
    i = 1
    try:
        mkdir(f"{_path}/cropped")
    except FileExistsError:
        pass

    for to_save in images:
        orig = to_save[0]
        crop = to_save[1:]

        for c in crop:
            aux = orig.crop(c)
            fname = f"{_path}/cropped/img{i:03d}.webp"
            aux.save(fname, 'WebP')
            print(f" saving {fname}")
            i += 1


def should_split(width, height):
    return width > height


def find_borders(img: Image) -> tuple:
    _h = img.height
    img_array = np.array(img.convert('L'))
    col_sum = np.sum(img_array, axis=0)

    full_white = 255 * _h
    threshold = full_white * 0.98

    left_border = np.where(col_sum < threshold)[0][0]
    right_border = np.where(col_sum[::-1] < threshold)[0][-1]

    return (left_border, right_border)


parser = argparse.ArgumentParser()
parser.add_argument("path")

args = parser.parse_args()

load_image(args.path)
