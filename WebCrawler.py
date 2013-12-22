from classlib import *
from bs4 import BeautifulSoup
import requests
import re

def main():
    base_url = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/'
    top_level = 'sponsors.htm'
    
    r = requests.get(base_url + top_level)
    soup = BeautifulSoup(r.text, 'html5lib')
    
    links = soup.find_all('li')
    departments = []
    for link in links:
        departments.append(link.a.get("href"))
        
    
    
    
    
    class_list = []
    for dpt in departments:
        page = requests.get(base_url + departments[9])
        s = BeautifulSoup(page.text, 'html5lib')     
        classes = s.find_all('tr')[3:]        
    
        for row in classes:
            col = row.find_all('td')
            if (len(col) < 8): #Ignores canceled classes
                continue
            if (re.match('[A-Z]{3}[0-9]{3}(H|Y)1', str(col[0].string))):
                code = col[0].string
                sem = col[1].string
                name = str(col[2].string)
                if (not re.match("[a-zA-Z\s]*", name)):
                    name = _extractBroken(name)     
                curr = Class(code, sem, name)
                class_list.append(curr)
            
            if (re.match('L[0-9]{4}', str(col[3].string))):
                code = str(col[3].string)        
                
                if (col[5].string != None):
                    time = str(col[5].string)
                else:
                    x = str(col[5].strong)
                    time = _extractBrokenTime(x)
                    
                if (col[6].string != None):
                    loc = str(col[6].string)
                else:
                    x = str(col[6].strong)
                    if (x != "None"):
                        loc =_extractBrokenLoc(str(col[6]))
                    else:
                        x = str(col[6].font)
                        loc = _multipleRooms(x)
                        
                    
                instruct = str(col[7].string)
                sec = LectureSection(code, instruct)
                for slot in _generateTimeSlot(time, loc):
                    sec.addTime(slot)
                class_list[-1].addLec(sec)
            elif (re.match('P[0-9]{4}', str(col[3].string))):
                code = str(col[3].string)        
                                
                if (col[5].string != None):
                    time = str(col[5].string)
                else:
                    x = str(col[5])
                    time = _extractBrokenTime(x)
                                    
                if (col[6].string != None):
                    loc = str(col[6].string)
                else:
                    x = str(col[6])
                    if (x != "None"):
                        loc =_extractBrokenLoc(x)
                    else:
                        x = str(col[6].font)
                        loc = _multipleRooms(x)
                                        
                                    
                instruct = str(col[7].string)
                sec = PracticalSection(code, instruct)
                for slot in _generateTimeSlot(time, loc):
                    sec.addTime(slot)
                class_list[-1].addLec(sec)                
            elif (re.match('T[0-9]{4}', str(col[3].string))):
                code = str(col[3].string)
                
                if (col[5].string != None):
                    time = str(col[5].string)
                else:
                    x = str(col[5])
                    time = _extractBrokenTime(x)
                    
                if (col[6].string != None):
                    loc = str(col[6].string)
                else:
                    x = str(col[6])
                    loc = _extractBrokenLoc(x)
                    
                class_list[-1].addTut(
                    TutorialSection(code, _generateTimeSlot(time, loc)[0]))
            else:
                if (col[5].string != None):
                    time = str(col[5].string)
                else:
                    x = str(col[5])
                    time = _extractBrokenTime(x)
                    
                if (col[6].string != None):
                    loc = str(col[6].string)
                else:
                    x = str(col[6].strong)
                    if (x != "None"):
                        loc =_extractBrokenLoc(str(col[6]))
                    else:
                        x = str(col[6].font)
                        loc = _multipleRooms(x)
                        
                    
                instruct = str(col[7].string)
                for slot in _generateTimeSlot(time, loc):
                    sec.addTime(slot)          
            
    return class_list




def _generateTimeSlot(time, loc):
    if (time != "TBA"):
        l , s = [], ''

        for char in time:
            if (re.match("[A-Z]", char)):
                l.append(char)
            else:
                s += char
                
        
        if (re.match("[1-9]:[0-9]{2}-[1-9]:[0-9]{2}", s)):
            start = (int(s[0]) + (int(s[2:4]) / 60)) + 12
            end = (int(s[5]) + (int(s[7:9]) / 60)) + 12
        elif (re.match("9-(10|11|12)", s)):
            start, end = int(s[0]), int(s[2:])
        elif (re.match("(10|11)-(11|12)", s)):
            start, end = int(s[:2]), int(s[2:])
        elif (re.match("(10|11|12)-[1-9]", s)):
            start, end = int(s[:2]), (int(s[-1]) + 12)
        elif (re.match("[1-9]-[1-9]", s)):
            start, end = (int(s[0]) + 12), (int(s[-1]) + 12)            
        elif (re.match("[1-9][0-9]{0,1} (p)", s)):
            start = int(s[:-3]) + 12
            end = start + 1
        elif (re.match("[10|11|12]", s)):
            start = int(s[:2])
            end = start + 1
        elif (re.match("[1-8]", s)):
            start = int(s[0]) + 12
            end = start + 1
        elif (re.match("9", s)):
            start = int(s[0])
            end = start + 1            
        else:
            raise Exception("No regex matched the time format")
        
        if (re.match("\(p\)", s)):
            start += 12
            end += 12
            
        return [TimeSlot(t, loc, start, end) for t in l]
            
    else:
        return [TBA]


def _extractBrokenLoc(string):
    match = re.search("[A-Z]{2} [A-Z]*[0-9]+", string)
    return match.group(0)

def _extractBrokenTime(string):
    match = re.search("(M|T|W|R|F)+[0-9]+:*[0-9]*-*[0-9]*:*[0-9]* ?(\(p\))*", 
                      string)
    return match.group(0)
    

def _multipleRooms(string):
    new_string, i, check, n = "", 0, False, 0
    while (True):
        if (n < 2):
            if (string[i] == ">"):
                check = True
                i += 1
                continue
            elif (check == True):
                if (string[i] == "<"):
                    i += 1
                    n += 1
                    check = False
                else:
                    if (string[i] == '\n'):
                        i += 1
                    else:
                        new_string += string[i]
                        i += 1
            else:
                i += 1
        else:
            break
        
    return new_string 
    
if __name__ == "__main__":
    x = main()
    for i in x:
        print(i.verbose())