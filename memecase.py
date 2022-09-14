#! /usr/bin/env python3

import sys
import argparse
import random
from time import time

try:
    import pyperclip
except ModuleNotFoundError:
    print("Module pyperclip not installed. Use `pip install pyperclip` to use this scrip.")
    sys.exit(1)

# actually randomize things every time we use the script...
random.seed(time())


def getFileContent(fn):
    with open(fn, 'r') as fp:
        return fp.read()

def main(content: str, n:int = 1, rand:bool=False, verbose:bool=False) -> None:
    content = content.split(' ')
    cnt = 0

    for i in range(len(content)):
        new_word = list(content[i])
        for j in range(len(new_word)):
            if rand:
                if random.random() > 0.5:
                    new_word[j] = new_word[j].upper()
            else:
                if cnt % (n + 1) == 0:
                    new_word[j] = new_word[j].upper()
            cnt += 1
        content[i] = ''.join(new_word)

    content = ' '.join(content)

    pyperclip.copy(content)

    if verbose:
        print(content)
        return
    print("Copied to clipboard. Meme away!\n")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', dest='text', action='store_true', help='')
    parser.add_argument('-c', '--clipboard', dest='clip', action='store_true', help='Get content from clipboard')
    parser.add_argument('-r', '--random', dest='random', action='store_true', help='Randomizes the pattern of \
        lower and upper cases')
    parser.add_argument('-n', dest='pattern', metavar='N', action='store', default=1, type=int, help='Changes the pattern \
        for when to change to a upper')
    parser.add_argument('-v', '--verbose', action='store_true', help='Specify if you want to print out the result.')
    parser.add_argument('-f', '--file', dest='file', action='store', help='gets text from a file')
    args = parser.parse_args()


    if args.text:
        content = input("Please enter what you want to memefy: ")
    elif args.clip:
        content = pyperclip.paste().lower()
    elif args.file:
        content = getFileContent(args.file)
    else:
        parser.print_help()
    main(content, n=args.pattern, rand=args.random, verbose=args.verbose)
