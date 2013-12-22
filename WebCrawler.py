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
        name = str(col[2].string)
        if (not re.match("[a-zA-Z\s]*", name)):
            name = _extractBroken(name)     
        curr = Class(code, sem, name)
        class_list.append(curr)
    
    if (re.match(lecture_code_regex, col[3].string[0])):
        code = str(col[3].string)        
        
        
        if (col[5].string != None):
            time = str(col[5].string)
        else:
            time = _extractBroken(str(col[5].string.strong))
            
        if (col[6].string != None):
            loc = str(col[5].string)
        else:
            loc = _extractBroken(str(col[6].string.strong))
            
        instruct = str(col[7].string)
        if (not re.match("L[0-9]{4}", code)):
            lec.addTime(time, loc)
        else:
            lec = LectureSection(code, time, loc, instruct)
            class_list[-1].addLec(lec)
                       
    else:
        code = str(col[3].string)
        
        if (col[5].string != None):
            time = str(col[5].string)
        else:
            time = _extractBroken(str(col[5].string.strong))
            
        if (col[6].string != None):
            time = str(col[5].string)
        else:
            time = _extractBroken(str(col[6].string.strong))
            
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
        else:
            raise Exception("Not regex matched the time format")
              
        for t in l:
            TimeSlot(t, loc, start, end)
        
        return l
    else:
        return TBA

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