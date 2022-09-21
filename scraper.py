USER_AGENT="User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
COOKIES = {"snip"}

import requests
from time import sleep

# rice
import progressbar

with open('index_12.m3u8', 'r') as fp:
    links = fp.read().split('\n')

s = requests.Session()

bar = progressbar.ProgressBar(maxval=len(links), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

for i in range(len(links)):
    fn = links[i].split('/')[-1]
    resp = s.get(links[i], cookies=COOKIES)
    if resp.status_code != '200':
        print(f'{fn}->{resp.status_code}')
        break
    fp = open(fn, 'wb')
    fp.write(resp.content)
    fp.close()
    bar.update(i+1)
    sleep(2)

bar.finish()
