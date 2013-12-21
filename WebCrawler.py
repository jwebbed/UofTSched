from classlib import *
from bs4 import BeautifulSoup
import requests
import re


base_url = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/'
top_level = 'sponsors.htm'

r = requests.get(base_url + top_level)
soup = BeautifulSoup(r.text, 'html5lib')

links = soup.find_all('li')
departments = []
for link in links:
    departments.append(link.a.get("href"))
    
regx = '[A-Z]{3}[0-9]{3}(H|Y)1'

page = requests.get(base_url + departments[0])
s = BeautifulSoup(page.text, 'html5lib')


classes = s.find_all('tr')[3:]

class_list = []
for row in classes:
    col = row.find_all('td')
    if (len(col) < 8):
        continue
    if (re.match(regx, col[0].string)):
        code = col[0].string
        sem = col[1].string
        name = col[2].string
        curr = Class(code, sem, name)
        class_list.append(curr)
    

    
    if (col[3].string[0] == L):
        code = col[3].string
        time = col[5].string
        loc = col[6].string
        struct = col[7].string
        class_list[-1].addLec(LectureSection(code, time, loc, struct))
    else:
        code = col[3].string
        time = col[5].string
        loc = col[6].string
        class_list[-1].addTut(TutorialSection(code, time, loc))               