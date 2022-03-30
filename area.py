import argparse
import sys
import subprocess
import shlex
from re import findall
from shutil import which

# default wacom ctl-480 width and heigh values
WIDTH = 15200
HEIGHT = 9500
RATIO = 1.78    # 16:9 ratio
DEVICE_NAME = "Wacom Intuos S Pen stylus"

def set_area(_values: tuple):
    left_w, top_h, right_w, bottom_h = _values
    _cmd = f"{which('xsetwacom')} --set \"{DEVICE_NAME}\" Area {left_w} {top_h} {right_w} {bottom_h}"
    subprocess.run(shlex.split(_cmd), capture_output=True, check=True)


def check_for_tablet():
    _cmd = f"{which('xsetwacom')} --list"
    ret = subprocess.run(shlex.split(_cmd), capture_output=True, check=True)
    _ret = ret.stdout.decode('utf-8')
    if _ret == '' or len(findall(DEVICE_NAME, _ret)) == 0:
        return False
    return True


def height_from_width(width: int):
    return int(width // RATIO)


def get_midpoint(max_width:int , max_height:int) -> int:
    return (max_width // 2, max_height // 2)


def make_box(width):
    height = height_from_width(width)
    midpoint_w, midpoint_h = get_midpoint(WIDTH, HEIGHT)
    half_w = width // 2
    half_h = height // 2

    _vals = (midpoint_w - half_w, midpoint_h - half_h, midpoint_w + half_w, midpoint_h + half_h)

    set_area(_vals)


def main():
    args = argparse.ArgumentParser()
    args.add_argument('width', action='store', type=int,)

    if check_for_tablet():

        parser = args.parse_args()
        make_box(parser.width)


main()

