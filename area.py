import sys
import subprocess
import shlex
from shutil import which

# default wacom ctl-480 width and heigh values
WIDTH = 15200
HEIGHT = 9500
RATIO = 1.78    # 16:9 ratio
DEVICE_NAME = "Wacom Intuos S Pen stylus"

def set_area(_values: tuple):
    """sets area on the tablet using subprocess.

    Args:
        _values (tuple): list of needed values
    """
    l_w, t_h, r_w, b_h = _values
    print("amipwned.py")
    _cmd = f"{which('xsetwacom')} --set \"{DEVICE_NAME}\" Area {l_w} {t_h} {r_w} {b_h}"
    subprocess.run(shlex.split(_cmd), capture_output=True, check=True)


def height_from_width(width: int):
    """Calculates the height from width given using RATIO

    Args:
        width (int): value of width

    Returns:
        int: calculated height value
    """
    return int(width // RATIO)


def get_midpoint(max_width:int , max_height:int) -> int:
    """Calculates midpoint for the rectangle with given width and height

    Args:
        max_width (int): max width
        max_height (int): max height

    Returns:
        tuple: middle point
    """
    middle = (max_width // 2, max_height // 2)

    return middle


def make_box(width):
    """Calculates the corner values

    Args:
        width (int): resized width
    """
    h = height_from_width(width)
    m_w, m_h = get_midpoint(WIDTH, HEIGHT)
    half_w = width // 2
    half_h = h // 2

    _vals = (m_w - half_w, m_h - half_h, m_w + half_w, m_h + half_h)

    set_area(_vals)

w = int(sys.argv[1])

make_box(w)