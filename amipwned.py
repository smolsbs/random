#! python
#!/usr/bin/python

# imports
import sys
from hashlib import sha1
from requests import get
from tkinter import Tk

def help():
    return """Usage:
    python amipwned.py \"password\";
    python amipwned.py [-c|--clipboard]"""


def hashMyPass():
    """Computes a password into it's SHA-1 hash and sends the first 5 chars to haveibeenpwned API, then checks all the responses from the
    server against the password hash to see if it's in the haveibeenpwned database."""



    # check if user has a password in the arguments
    # if not, throw an exception
    if len(sys.argv)  != 2:
        raise Exception("No argument passed.\n\n{}".format(help()))
    
    if sys.argv[1].lower() in  ['-c','--clipboard']:
        pwd = Tk().clipboard_get().encode('utf-8')
    else:
        #  prepares password string to utf-8
        pwd = sys.argv[1].encode('utf-8')

    # hashes the password and returns it's hexdigest
    hashedPwd = sha1(pwd).hexdigest()

    # firsts 5 chars of the hash
    hashPre = hashedPwd[:5]

    # sends a GET request to the API and retrieves the response
    # then checks if it's a 200 GET response
    req = get('https://api.pwnedpasswords.com/range/' + hashPre)
    if req.status_code != 200:
        print("Unable to retrieve a response. Got a {:%d} response".formar(req.status_code))

    # splits every hash got from the server and iterates over it, checking against our password hash
    for h in req.text.split('\n'):
        
        h = h.split(':')        # format=> hash:nOccurrences

        if hashedPwd == hashPre + h[0].lower():
            print("Hash {} found. Number of occurrences: {}".format(hashedPwd, h[1]))
            return
    print("pwd not found. Congrats!")
    return


if __name__ == '__main__':
    hashMyPass()