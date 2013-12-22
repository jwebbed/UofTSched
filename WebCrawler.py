from classlib import *
from bs4 import BeautifulSoup
import requests
import re

#Constants
base_url = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/'
top_level = 'sponsors.htm'
course_code_regex = '[A-Z]{3}[0-9]{3}(H|Y)1'
lecture_code_regex = 'L[0-9]{4}'
tutorial_code_regex = 'T[0-9]{4}'

r = requests.get(base_url + top_level)
soup = BeautifulSoup(r.text, 'html5lib')

links = soup.find_all('li')
departments = []
for link in links:
    departments.append(link.a.get("href"))
    


page = requests.get(base_url + departments[0])
s = BeautifulSoup(page.text, 'html5lib')


classes = s.find_all('tr')[3:]

class_list = []
for row in classes:
    col = row.find_all('td')
    if (len(col) < 8): #Ignores canceled classes
        continue
    if (re.match(course_code_regex, col[0].string)):
        code = col[0].string
        sem = col[1].string
        name = col[2].string
        if (name == None):
            x = col[2].strong
            s = ""
            x = str(x)[8:]
            for char in x:
                if (char == "<"):
                    break
                else:
                    s += char
            name = s        
        curr = Class(code, sem, name)
        class_list.append(curr)
    
    if (re.match(lecture_code_regex, col[3].string[0])):
        code = col[3].string
        time = col[5].string
        if (time == None):
            x = col[5].strong
            
            time = s
        loc = col[6].string
        if (loc == None):
                    x = col[6].strong
                    s = ""
                    x = str(x)[8:]
                    for char in x:
                        if (char == "<"):
                            break
                        else:
                            s += char
                    loc = s        
        struct = col[7].string
        if (not re.match("L[0-9]{4}", code)):
            lec.addTime(time, loc)
        else:
            lec = LectureSection(code, time, loc, struct)
            class_list[-1].addLec(lec)
                       
    else:
        code = col[3].string
        time = col[5].string
        if (time == None):
                    x = col[5].strong
                    s = ""
                    x = str(x)[8:]
                    for char in x:
                        if (char == "<"):
                            break
                        else:
                            s += char
                    time = s        
        loc = col[6].string
        if (loc == None):
            x = col[6].strong
            s = ""
            x = str(x)[8:]
            for char in x:
                if (char == "<"):
                    break
                else:
                    s += char
            loc = s         
        class_list[-1].addTut(TutorialSection(code, time, loc)) 




def _generateTimeSlot(time, loc):
    if (time != "TBA"):
        l , s = [], ''

        for char in time:
            if (re.match("[A-Z]", char)):
                l.append(char)
            else:
                s += char
        
    if (re.match("9-[10|11|12]", s)):
        start, end = int(s[0]), int(s[2:])
    elif (re.match("[10|11]-[11|12]", s)):
        start, end = int(s[:2]), int(s[2:])
    elif (re.match("[10|11|12]-[1-9]", s)):
        start, end = int(s[:2]), (int(s[-1]) + 12)
    elif (re.match("[1-9][0-9]{0,1} (p)", s)):
        start = int(s[:-3]) + 12
        end = start + 1
    elif (re.match("[9|10|11|12]", s)):
        start = int(s)
        end = start + 1
    elif (re.match("[1-9]", s)):
        start = int(s) + 12
        end = s + 1
          
    for t in l:
        TimeSlot(t, loc, start, end)
    
    return l

def _extractBroken(string):
    new_string = ""
    i = 0
    check = False
    while (true):
        if (string[i] == ">"):
            check = True
            continue
        elif (check == True):
            if (string[i] == "<"):
                break
            else:
                new_string += string[i]
                i += 1
        else:
            i += 1
        
    return new_string   

if __name__ == "__main__":
    for i in class_list:
        print(i.verbose())