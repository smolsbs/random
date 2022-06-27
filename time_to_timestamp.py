#! /usr/bin/env python3

import argparse
from datetime import datetime
from math import floor
from sys import exit

try:
    import pyperclip
    import pytz
except ModuleNotFoundError:
    print("Module pyperclip or pytz not installed. Use `pip install pyperclip pytz` to use this scrip.")
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

def construct_ts(ts: int, flags: list) -> list:
    aux = []
    for flag in flags:
        aux.append(f'<t:{ts}:{flag}>')

    return aux

def parse_flags(args: argparse.Namespace) -> list:
    aux = vars(args)
    flags = list(k for k,v in aux.items() if v is True)
    if len(flags) == 0:
        raise Exception("No flags specified")
    return sorted(flags) # just for concistency sake when creating the timestamps

def main(args: argparse.Namespace) -> None:
    flags = parse_flags(args)
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
    parser.add_argument('--timezone', '-tz', action='store', type=str, default=None, help="See https://timezonedb.com/time-zones for names of each time zone.")

    parser.add_argument('-f', action='store_true', help="long date with short time")
    parser.add_argument('-F', action='store_true', help="long date with day of the week and short time")
    parser.add_argument('-R', action='store_true', help="relative time")
    parser.add_argument('-t', action='store_true', help="short time")
    parser.add_argument('-T', action='store_true', help="long time")
    parser.add_argument('-d', action='store_true', help="short date")
    parser.add_argument('-D', action='store_true', help="long date")

    args = parser.parse_args()
    main(args)
