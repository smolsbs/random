#! /usr/bin/env python3

import argparse
import concurrent.futures
import os
import shlex
import sys
import threading
from os.path import basename, join, splitext
from pathlib import Path
from shutil import which
from subprocess import run

VALID_FORMATS = {'.flac', '.wav', '.aiff'}
FORMAT_BIN = {'opus': ('opusenc', "--quiet --bitrate 160", 'opus'),
              'flac': ('flac', "-s -l 8 -b 4096 -M -r 4 --keep-foreign-metadata -o", 'flac'),
              'ogg': ('oggenc', "--quiet -q 5 -o", 'ogg')}
BASE_FOLDER = os.getcwd()


class NoValidFiles(Exception):
    def __init__(self, lyst ,message='No valid files were found to convert.'):
        self.lyst = lyst
        self.message = message
        super().__init__(lyst)

    def __str__(self) -> str:
        return f'{self.message}'


def get_files(_path: str):
    all_files = os.listdir(_path)
    valid_files = [f for f in all_files if splitext(f)[-1].lower() in VALID_FORMATS]
    if len(valid_files) == 0:
        raise NoValidFiles(valid_files)
    return sorted(valid_files)


def convert_single_folder(_path, _format, _n_threads):
    # TODO: copy the cover file if there's one to the output folder

    output_folder = join(Path(_path).parent, f"{basename(_path)} [{_format}]")

    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass

    files = get_files(_path)

    _enc, _args, _ext = FORMAT_BIN[_format]
    pool = []
    for _f in files:
        _fname = splitext(_f)[0]
        old_file = join(_path, _f)
        new_file = join(_path, f"{output_folder}/{_fname}.{_ext}")
        _cmd = shlex.split(f'{which(_enc)} \"{old_file}\" {_args} \"{new_file}\"')
        pool.append((_cmd, _fname))
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=min(_n_threads,8))
    for result in executor.map(thread_convert, pool):
        print(result)


def thread_convert(args):
    _cmd, _name = args
    proc = run(_cmd, capture_output=False, check=True)
    if proc.returncode != 0:
        print(f'Received process return code of {proc.returncode}. Stopping...')
        sys.exit(proc.returncode)
    return f'Finished converting {_name}'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--folder',
                        dest='folder',
                        action='store',
                        help='Folder to convert the files.')
    parser.add_argument('-t', '--threads',
                        dest='threads',
                        action='store',
                        default=6,
                        type=int)
    parser.add_argument('-e', '--encoder',
                        action='store',
                        default='opus',
                        help='Use the specified encoder. Avaliable encoding options are: opus; ogg; flac')
    

    args = parser.parse_args()

    if args.folder:
        path = join(BASE_FOLDER, args.folder)
        convert_single_folder(path, args.encoder, args.threads)

