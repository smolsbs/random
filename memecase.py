#! /usr/bin/env python3

import sys
import argparse
import random

try:
    import pyperclip
except ModuleNotFoundError:
    print("Module pyperclip not installed. Use `pip install pyperclip` to use this scrip.")
    sys.exit(1)


def main(content, n = 1, rand=False, verbose=False):
    content = list(content)
    for i in range(len(content)):
        if rand:
            if random.random() > 0.5:
                content[i] = content[i].upper()
        else:
            if i % (n + 1) == 0:
                content[i] = content[i].upper()
    content = ''.join(content)

    pyperclip.copy(content)

    if verbose:
        print(content)
        return
    print("Copied to clipboard. Meme away!\n")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', dest='text', action='store', help='')
    parser.add_argument('-c', '--clipboard', dest='clip', action='store_true', help='Get content from clipboard')
    parser.add_argument('-r', '--random', dest='random', action='store_true', help='Randomizes the pattern of \
        lower and upper cases')
    parser.add_argument('-n', dest='pattern', metavar='N', action='store', default=1, type=int, help='Changes the pattern \
        for when to change to a upper')
    parser.add_argument('-v', '--verbose', action='store_true', help='Specify if you want to print out the result.')
    args = parser.parse_args()


    if args.text:
        content = args.text
    elif args.clip:
        content = pyperclip.paste().lower()
    else:
        parser.print_help()
    main(content, n=args.pattern, rand=args.random, verbose=args.verbose)
