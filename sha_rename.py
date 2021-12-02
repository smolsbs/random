#! /usr/bin/env python3

import argparse

from hashlib import sha256
from os import getcwd, listdir
from os.path import isfile, join
from shutil import move

VALID_FORMATS = ['jpg', 'jpeg', 'png', 'bpm']

def renameFile(fn: list, size=12):
    parentDir = getcwd()
    for f in fn:
        ext = f.split('.')[1]
        sha = sha256()
        with open(f, 'rb') as fp:
            sha.update(fp.read())
            f_hash = sha.hexdigest()[:size]
        print(f'{f} -> {f_hash}.{ext}')
        move(join(parentDir, f), join(parentDir, f'{f_hash}.{ext}' ) ) 
    
    
def getFilesInDir(_dir):
    files = [f for f in listdir(_dir) if (isfile(join(_dir, f)) and f.split('.')[1] in VALID_FORMATS )]
    return files
    

def main():
    parser = argparse.ArgumentParser()
    req = parser.add_mutually_exclusive_group()
    req.add_argument('-a', '--all', action='store_true',default=True, dest='all')
    
    parser.add_argument('-n', action='store',  default=12, dest='size')
    parser.add_argument('-f', '--format', action='store', nargs='+')
    args = parser.parse_args()
    
    if args.all:
        allFiles = getFilesInDir(getcwd())
        renameFile(allFiles)
    elif args.files:
        pass    
    


if __name__ == '__main__':
    main()


