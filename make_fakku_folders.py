#! /usr/bin/env python3

import argparse
import json
import os
import shutil
from os.path import abspath, basename, dirname, isdir, isfile, splitext
from string import ascii_letters, digits
from zipfile import ZipFile

import requests

try:
    import progressbar
    USE_PROGRESSBAR = True
except ModuleNotFoundError:
    USE_PROGRESSBAR = False

VALID_CHARS = frozenset(r'()[]{}_!.- ' + ascii_letters + digits)
BASE_PATH = os.getcwd()
VALID_EXT = {'.zip', '.cbz'}

GOOD_TAGS = {'leg lock', 'vanilla', 'biting', 'orgasm denial', 'succubus', 'fangs'}
TRASH_TAGS = {'cheating', 'netorare', 'netorase', 'netori', 'bestiality', 'ugly bastard', 'swinging'}
DECENCY = {0: 'maybe', -1: 'trash', 1: 'good'}


def sanitize_string(_str:str ) -> str:
    """Removes any character that might cause problems with file
    systems

    Args:
        _str (str): string to sanitize

    Returns:
        str
    """    
    sanitized_str = str()
    for f in _str:
        if f in VALID_CHARS:
            sanitized_str += f
        else:
            sanitized_str += '_'
    
    return sanitized_str


def parse_json(json_file: bytes) -> dict:
    _data = json.loads(json_file)
    return _data


def dl_cover(url: str) -> None:
    _r = requests.get(url)

    if _r.status_code != 200:
        raise requests.HTTPError(_r.status_code)

    with open('cover.png', 'wb') as fp:
        fp.write(_r.content)


def get_local_cover(_fp: str) -> None:
    with ZipFile(_fp,'r') as zip_file:
        cover = zip_file.read('01.png')

    cover_fp = open('cover.png', 'wb')
    cover_fp.write(cover)
    cover_fp.close()


def write_into_json(data: dict) -> None:
    dets_dict = {"title": data["Title"],
                 "author": data["Artist"],
                 "artist": data["Artist"],
                 "description": data["Description"],
	             "genre": data["Tags"],
                 "status": "3",
                 "_status values": ["0 = Unknown", "1 = Ongoing", "2 = Completed", "3 = Licensed"]
                }

    dets = json.dumps(dets_dict)
    with open('details.json', 'w') as fp:
        fp.write(dets)


def get_info_from_zip(_fp: str) -> bytes:
    with ZipFile(_fp, 'r') as zip_file:
        # yeah, just keep the info.json file inside the archive.
        data = zip_file.read('info.json')
    return json.loads(data)


def create_entry(_file:str, dl_cover=True) -> None:
    # get filename and extension
    fname = splitext(_file)[0]

    # remove invalid chars and create the dir
    clean_fname = sanitize_string(fname)
    os.mkdir(clean_fname)
    new_file = f'{clean_fname}.cbz'

    # move the zip/cbz file to the created dir and change dir into it
    shutil.move(_file, f'{clean_fname}/{new_file}')
    os.chdir(clean_fname)

    # get the info.json from inside the zipped file and save it to details.json
    data = get_info_from_zip(new_file)
    write_into_json(data)

    # download the cover art
    if dl_cover:
        dl_cover(data['Thumb'])
    else:
        get_local_cover(new_file)

    # leave the created folder
    os.chdir('..')


def prepare_dir_and_fname(rel_dir: str) -> tuple:
    _abs_path = abspath(rel_dir)
    _dir = dirname(_abs_path)
    _fname = basename(_abs_path)
    return (_dir, _fname)


def get_files_from_folder(_dir: str) -> list:
    os.chdir(_dir)
    files = [f for f in os.listdir() if isfile(f)]
    os.chdir(BASE_PATH)

    return files


def get_folders(_dir: str) -> list:
    os.chdir(_dir)
    folders = [f for f in os.listdir() if isdir(f)]
    os.chdir(BASE_PATH)

    return folders


def check_if_sorting_folders_exit(folder_list: list) -> None:
    for _f in DECENCY.values():
        if _f not in folder_list:
            os.mkdir(_f)


def make_report(_report: dict, n_files: int) -> None:
    _fp = open('report.txt', 'w')

    _fp.write(f"Number of files processed: {n_files}\n")
    _fp.write(f"{'='*30}\nGood: {len(_report[1])}\n")
    for entry in sorted(_report[1]) :
        _fp.write(f"\n\t{entry}")
    _fp.write(f"\n{'='*30}\nMaybe: {len(_report[0])}\n")
    for entry in sorted(_report[0]):
        _fp.write(f"\n\t{entry}")
    _fp.write(f"\n{'='*30}\nTrash: {len(_report[-1])}\n")
    for entry in sorted(_report[-1],key=lambda x: x[0]):
        _entry, reason = entry
        _fp.write(f"\n\t{_entry} | Reason: {reason}")

    _fp.close()


def sort_entries(folder_list: list, test=False) -> None:
    final_sort = {-1: [], 0: [], 1: []}

    if not test:
        check_if_sorting_folders_exit(folder_list)

    print("Sorting...")
    for entry in folder_list:

        if entry in DECENCY.values():
            continue
        decency = 0

        with open(f'{entry}/details.json', 'r') as fp:
            tags = json.loads(fp.read())['genre']
        
        for tag in tags:
            _tag = tag.lower()
            if _tag in GOOD_TAGS:
                decency = 1
                continue
            elif _tag in TRASH_TAGS:
                decency = -1
                break   # don't even bother iterating over the remaining tags, it's trash anyway
        if not test:
            shutil.move(entry, f'{DECENCY[decency]}/')
        
        if decency == -1:
            final_sort[decency].append([entry, _tag])
        else:
            final_sort[decency].append(entry)

    print("Sorting has finished. A report.txt file has been created.")
    n_files = sum(map(len, final_sort.values()))
    make_report(final_sort, n_files)


def main(_list:list, dl_cover=False) -> None:
    if USE_PROGRESSBAR:
        _bar = progressbar.ProgressBar(maxval=len(_list),
                                      widgets=[progressbar.Bar('=', '[', ']'),
                                      ' ',
                                      progressbar.Percentage()])
        i = 0
        _bar.start()

    for _f in _list:
        _dir, _file = prepare_dir_and_fname(_f)
        if _dir != os.getcwd():
            os.chdir(_dir)

        ext = splitext(_file)[1]
        if ext not in VALID_EXT:
            continue

        create_entry(_file, dl_cover)
        if USE_PROGRESSBAR:
            i += 1
            _bar.update(i)

    if USE_PROGRESSBAR:
        _bar.finish()


if __name__ == "__main__":
    os.chdir(BASE_PATH)

    args = argparse.ArgumentParser()

    req_args = args.add_mutually_exclusive_group()
    req_args.add_argument('-j', '--json', action='store', dest='json',
                          help='Creates a info.json file from the zip archive passed')
    # req_args.add_argument('-f', '--files', action='store', nargs='+', dest='files',
    #                       help='Creates entries for the chosen files.')
    req_args.add_argument('-F', '--folder', action='store', dest='folder')

    args.add_argument('-s', '--sort', action='store', )
    args.add_argument('-dl', action='store_true', dest='cover')
    args.add_argument('--simulate', action='store_true', help='Simulates the sorting and creates the report.txt file.')

    parser = args.parse_args()

    if parser.json:
        parse_json(parser.json)
    
    # pretty sure passing files is broken.
    # TODO: fix this
    # elif parser.files:
    #     main(parser.files)
    elif parser.folder:
        _files = get_files_from_folder(parser.folder)
        os.chdir(parser.folder)
        if parser.cover:
            main(_files, True)
        else:
            main(_files)
    
    if parser.sort:
        _folders = get_folders(parser.sort)
        os.chdir(parser.sort)
        sort_entries(_folders, parser.simulate)
