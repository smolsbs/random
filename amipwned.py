#!/usr/bin/env python3

# imports
import sys
from argparse import ArgumentParser
from hashlib import sha1

try:
    import pyperclip
except ModuleNotFoundError:
    print('Module pyperclip not installed. Please install it.')
    sys.exit(1)
from requests import get


def hashMyPass(pwd, verbose=False):
    """Computes a password into it's SHA-1 hash and sends the first 5 chars to haveibeenpwned API, then checks all the responses from the
    server against the password hash to see if it's in the haveibeenpwned database."""

    # hashes the password and returns it's hexdigest
    hashedPwd = sha1(pwd).hexdigest()
    if verbose:
        n_pwd = len(pwd)
        print(f'[*] Size of password: {n_pwd}')
        print(f'[*] First 6 chars of the hashed password: {hashedPwd[:6]}...')

    # firsts 6 chars of the hash
    hashPre = hashedPwd[:5]

    # sends a GET request to the API and retrieves the response
    # then checks if it's a 200 GET response
    req = get('https://api.pwnedpasswords.com/range/' + hashPre)
    if req.status_code != 200:
        print("Unable to retrieve a response. Got a {:%d} response".format(req.status_code))
    if verbose:
        print(f'[*] 200 OK from api.pwnedpasswords.com')
    # splits every hash got from the server and iterates over it, checking against our password hash
    all_hashes = req.text.split('\n')
    if verbose:
        n_hashes = len(all_hashes)
        print(f'[*] number of hashes returned: {n_hashes}')

    for h in all_hashes:
        h = h.split(':')        # format=> hash:nOccurrences

        if hashedPwd == hashPre + h[0].lower():
            print("Hash {} found. Number of occurrences: {}".format(hashedPwd, h[1]))
            return
    print("pwd not found. Congrats!")
    return


if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument('-c', dest='clip', action='store_true', help='get password from clipboard')
    args.add_argument('-t', dest='pw',action='store', help='input the password as an argument')
    args.add_argument('-v', '--verbose', action='store_true', help='Increases the verbosity of the output')
    parser = args.parse_args()

    content = ''
    verb = False

    if parser.clip:
        content = pyperclip.paste().encode('utf-8')
    elif parser.pw:
        content = parser.pw.encode('utf-8')

    if parser.verbose:
        verb = True

    hashMyPass(content, verb)
