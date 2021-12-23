#! /usr/bin/env python3

import argparse
from datetime import datetime
from math import floor
from sys import exit

try:
    import pyperclip
except ModuleNotFoundError:
    print("Module pyperclip not installed. Use `pip install pyperclip` to use this scrip.")
    exit(1)


AVAL_FLAGS = {'t': r'%I:%M %p',
              'T': r'%I:%M:%S %p',
              'd': r'%d/%m/%Y',
              'D': r'%d %B %Y',
              'f': r'%d %B %Y %I:%M %p',
              'F': r'%A, %d %B, %Y %I:%M %p',
              'R': r''}

def to_relative(_ts: int):
    _delta = datetime.fromtimestamp(_ts) - datetime.today()

    print(_delta.days)
    if _delta.days > 1:
        asdf = datetime.strptime(str(_delta), "%j days, %H:%M:%S.%f")
    elif _delta.days == 1:
        asdf = datetime.strptime(str(_delta), "%j day, %H:%M:%S.%f")
    else:
        asdf = datetime.strptime(str(_delta), "%H:%M:%S.%f")

    if asdf.month > 1:
        _str = f'in {asdf.month} months'
    elif asdf.month == 1 and asdf.day > 1 :
        _str = f'in {asdf.day} days'
    elif asdf.day == 1 and _delta.days > 0:
        _str = f'in {asdf.day + 1} days'
    elif asdf.day == 1 and _delta.days == 0 and asdf.hour > 1:
        _str = f'in {asdf.hour} hours'
    elif asdf.day == 1 and asdf.hour == 1:
        _str = f'in {asdf.hour} hour'
    elif asdf.hour < 1 and asdf.minute > 1:
        _str = f'in {asdf.minute} minutes'
    elif asdf.hour < 1 and asdf.minute <= 1:
        _str = f'in {asdf.minute} minute'

    return _str

def convert_time_to_ts(_time):
    _t = datetime.fromisoformat(' '.join(_time))

    return floor(_t.timestamp())


def construct_ts(_ts: int, flags: list) -> list:
    _aux = []
    for flag in flags:
        _aux.append(f'<t:{_ts}:{flag}>')

    return _aux

def parse_flags(_flags: str) -> list:
    parsed_flags = []
    for _f in _flags:
        if _f not in AVAL_FLAGS.keys():
            raise Exception(f'{_f} is not a valid flag. See example for valid flags.')
        parsed_flags.append(_f)
    return parsed_flags


def main(_args):
    _flags = parse_flags(_args.flags)
    _ts = convert_time_to_ts(_args.time)
    ts_list = construct_ts(_ts, _flags)
    # if _args.verbose:
    #     pretty_print(ts_list)

    _ret = ' '.join(ts_list)
    pyperclip.copy(_ret)
    print(_ret)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('time', nargs='+' ,action='store',
                        help="Input the datetime to convert, using the ISO format.")
    parser.add_argument('-f', '--flags', action='store', type=str, required=True,
                        help='Valid flags  tTdDfFR')

    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    main(args)
