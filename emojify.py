from PIL import Image
from itertools import product
import cv2
import numpy
import os
import re
import shutil

valid_images = {'.bmp', '.jpg', '.jpeg', '.png', '.ppm', '.pbm', '.pnm', '.pgm', '.tiff', '.tif', '.webp', }

w = 0
h = 0
n = 0


# https://stackoverflow.com/questions/5953373/how-to-split-image-into-multiple-pieces-in-python
def tile(filename, dir_in, dir_out):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    global w, h, n
    w, h = img.size

    nInput = input(f"Image size is {w} by {h} pixels. What is your resolution in pixels? ")
    while (not nInput.isnumeric()) or (int(nInput) >= w or int(nInput) >= h):
        nInput = input("Invalid input. What is your resolution in pixels? ")
    n = int(nInput)

    grid = product(range(0, h - h % n, n), range(0, w - w % n, n))
    for i, j in grid:
        box = (j, i, j + n, i + n)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)


def nearestNeighbor(r, g, b):
    colors = {'black': ((0, 0, 0), ":black_large_square:"), 'white': ((255, 255, 255), ":white_large_square:"),
              'red': ((255, 0, 0), ":red_square:"), 'green': ((0, 255, 0), ":green_square:"),
              'blue': ((0, 0, 255), ":blue_square:"), 'orange': ((255, 165, 0), ":orange_square:"),
              'yellow': ((255, 255, 0), ":yellow_square:"), 'purple': ((106, 13, 173), ":purple_square:"),
              'brown': ((139, 69, 19), ":brown_square:")}

    minDist = 255 * 3 + 1
    color = ''
    for i in colors:
        rgb = colors[i][0]
        dist = abs(rgb[0] - r) + abs(rgb[1] - g) + abs(rgb[2] - b)
        if dist < minDist:
            minDist = dist
            color = i
    return colors[color][1]


filepath = input("Enter the path to the file you want to turn to emoji:\n").strip()

while (not os.path.isfile(filepath) or (os.path.splitext(filepath)[1] not in valid_images)):
    filepath = input(
        filepath + " is not a valid image file. Enter the path to the file you want to turn to emoji:\n").strip()

file = os.path.basename(filepath)
print(file)
filename, ext = os.path.splitext(file)

dirPath = "TiledImages"
if (os.path.isdir(dirPath)):
    shutil.rmtree("TiledImages")
os.mkdir(dirPath)

tile(file, re.sub(f'{file}$', '', filepath), dirPath)

os.chdir(dirPath)
with open('../out.txt', 'w') as f:
    for i in range(0, h - h % n, n):
        for j in range(0, w - w % n, n):
            fn = f'{filename}_{i}_{j}{ext}'
            # print(fn)
            # https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
            myimg = cv2.imread(fn)
            avg_color_per_row = numpy.average(myimg, axis=0)
            avg_color = numpy.average(avg_color_per_row, axis=0)

            # print(avg_color,end='')
            emo = nearestNeighbor(avg_color[1], avg_color[2], avg_color[0])
            # print(emoji, end = '')
            f.write(emo)
        f.write('\n')
    f.close()
