import sched, time
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import os

c = 'united-states'

def trends(c):
    p='in'
    page='trends24'
    plus=c
    url='https://www.'+page+'.'+p+'/'+plus
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            #'authority': 'scrapeme.live',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
    )
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read(), 'html.parser')
    rows = soup.find_all('li')
    tr=[]
    for row in rows[:10]:          # Print all occurrences
       tr.append(row.get_text())
    return tr


def write_trends(tr):
    fn="log.txt"
    if os.path.exists(fn):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    log = open(fn, append_write)
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    log.write("date and time = " + dt_string + "\n")
    for t in tr: 
        print(t)
        log.write(t+ "\n")


t_list=trends(c)
write_trends(t_list)    

s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    t_list=trends(c)
    write_trends(t_list) 
    s.enter(60, 1, do_something, (sc,))

s.enter(60*20, 1, do_something, (s,))
s.run()


log.close()
