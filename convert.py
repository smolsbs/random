#! /usr/bin/env python3

import argparse
import os
import shlex
import sys
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
    """Class constructor for NoValidFiles exception

    Args:
        Exception (Expection): Buil-in class
    """    
    def __init__(self, lyst ,message='No valid files were found to convert.'):
        self.lyst = lyst
        self.message = message
        super().__init__(lyst)

    def __str__(self) -> str:
        return f'{self.message}'


def get_files(_path: str):
    """Retrieves all the valid files from the current directory set

    Args:
        _path (str): Path for retrieving the files

    Raises:
        NoValidFiles: Error in case no valid files were found

    Returns:
        list: Array of all the files found
    """
  
    all_files = os.listdir(_path)
    valid_files = [f for f in all_files if splitext(f)[-1].lower() in VALID_FORMATS]
    if len(valid_files) == 0:
        raise NoValidFiles(valid_files)
    return sorted(valid_files)


def convert_single_folder(_path, _format):
    """Converts the files

    Args:
        _path (str): Path where the files are
        _format (str): encoder to use
    """
    # TODO: copy the cover file if there's one to the output folder

    output_folder = join(Path(_path).parent, f"{basename(_path)} [{_format}]")

    try:
        os.mkdir(output_folder)
    except FileExistsError:
        pass

    files = get_files(_path)

    _enc, _args, _ext = FORMAT_BIN[_format]

    for _f in files:
        _fname = splitext(_f)[0]

        old_file = join(_path, _f)
        new_file = join(_path, f"{output_folder}/{_fname}.{_ext}")

        _cmd = shlex.split(f'{which(_enc)} \"{old_file}\" {_args} \"{new_file}\"')
        print(f'Converting {_f}...')
        proc = run(_cmd, capture_output=False, check=True)
        if proc.returncode != 0:
            print(f'Received process return code of {proc.returncode}. Stopping...')
            sys.exit(proc.returncode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--folder',
                        dest='folder',
                        action='store',
                        help='Folder to convert the files.')
    parser.add_argument('-e', '--encoder',
                        action='store',
                        default='opus',
                        help='Use the specified encoder. Avaliable encoding options are: opus; ogg; flac')
    

    args = parser.parse_args()

    if args.folder:
        path = join(BASE_FOLDER, args.folder)
        convert_single_folder(path, args.encoder)

