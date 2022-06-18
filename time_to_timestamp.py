#! /usr/bin/env python

import argparse
from datetime import datetime
from math import floor
from sys import exit

try:
    import pyperclip
    import pytz
except ModuleNotFoundError:
    print("Module pyperclip not installed. Use `pip install pyperclip` to use this scrip.")
    exit(1)

DFT_TZ = "Europe/Lisbon"        # Change this to your local timezone

AVAL_FLAGS = {'t': r'%I:%M %p',
              'T': r'%I:%M:%S %p',
              'd': r'%d/%m/%Y',
              'D': r'%d %B %Y',
              'f': r'%d %B %Y %I:%M %p',
              'F': r'%A, %d %B, %Y %I:%M %p',
              'R': r''}


def convert_time_to_ts(time: str, tz: str=None) -> int: 
    dumb_time = datetime.fromisoformat(' '.join(time))
    
    local_tz = pytz.timezone(DFT_TZ)
    if tz:
        remote_tz = pytz.timezone(tz)
        loc_time = remote_tz.localize(dumb_time).astimezone(local_tz)
    else:
        loc_time = local_tz.localize(dumb_time)
    
    return floor(loc_time.timestamp())

def help_print_flag_meanings():
    help = "t: short time; T: long time; d: short date; D: long date; f: long date with short time; F: long date with day of the week and short time; R: relative time"
    return help


def construct_ts(ts: int, flags: list) -> list:
    aux = []
    for flag in flags:
        aux.append(f'<t:{ts}:{flag}>')

    return aux

def parse_flags(flags: str) -> list:
    parsed_flags = []
    for _f in flags:
        if _f not in AVAL_FLAGS.keys():
            raise Exception(f'{_f} is not a valid flag. See example for valid flags.')
        parsed_flags.append(_f)
    return parsed_flags


def main(args: argparse.Namespace) -> None:
    flags = parse_flags(args.flags)
    ts = convert_time_to_ts(args.time, args.timezone)

    ts_list = construct_ts(ts, flags)

    ret = ' '.join(ts_list)
    print(ret)
    pyperclip.copy(ret)
    print("Timestamps copied to clipboard.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('time', nargs='+' ,action='store',
                        help="Input the datetime to convert, using the ISO format. (YYYY-mm-dd HH:mm[:ss])")
    parser.add_argument('--timezone', '-tz', action='store', type=str, default=None)
    parser.add_argument('-f', '--flags', action='store', type=str, required=True,
                        help=f"Can be a string of multiple flags.\nAvaliable flags: {help_print_flag_meanings()}")

    args = parser.parse_args()
    main(args)
