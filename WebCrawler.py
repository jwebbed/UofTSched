from classlib import *
from bs4 import BeautifulSoup
import requests
import re
import math
import traceback

def main():
    base_url = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/'
    top_level = 'sponsors.htm'
    
    r = requests.get(base_url + top_level)
    soup = BeautifulSoup(r.text, 'html5lib')
    
    links = soup.find_all('li')
    departments = []
    for link in links:
        departments.append(link.a.get("href"))
        
    
    
    
    try:
        class_list = []
        for dpt in departments:
            page = requests.get(base_url + dpt)
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
    except:
        print(class_list[-1].code)
        traceback.print_stack()
            
    return class_list
   
    



def _generateTimeSlot(time, loc):
    if (time != "TBA"):
        l , s = [], ''

        for char in time:
            if (re.match("[A-Z]", char)):
                l.append(char)
            else:
                s += char
                
        
        if (not re.match("-", s)):
            if (re.match(":", s)):
                match = re.search("[0-9]{1,2}:[0-9]{2}:", s)
                t = match.group(0)
                parts = t.split(':')
                start = int(parts[0])
                if (start < 9):
                    start += 12
                start *= 4
                start += math.round(int(parts[1])/15)
                end = start + 4
            elif (re.match("[0-9]{1,2}", s)):
                match = re.search("[0-9]{1,2}", s)
                t = match.group(0)
                start = int(t)
                if (start < 9):
                    start += 12
                start *= 4
                end = start + 4
            elif(re.match("-", s)):
                if (re.match(":", s)):
                    match = re.search("[0-9]{1,2}:[0-9]{2}:", s)
                    
                    t = match.group(0)
                    parts = t.split(':')
                    start = int(parts[0])
                    if (start < 9):
                        start += 12
                    start *= 4
                    start += math.round(int(parts[1])/15)
                    
                    t = match.group(1)
                    parts = t.split(':')
                    end = int(parts[0])
                    if (end < 9):
                        end += 12
                    end *= 4
                    end += math.round(int(parts[1])/15)                  
            elif (re.match("[0-9]{1,2}", s)):
                match = re.search("[0-9]{1,2}", s)
                
                t = match.group(0)
                start = int(t)
                if (start < 9):
                    start += 12
                start *= 4
                
                t = match.group(1)
                end= int(t)
                if (end < 9):
                    end += 12
                end *= 4
        
     
        if (re.match("\(p\)", s)):
            start += 12
            end += 12
            
        return [TimeSlot(t, loc, start, end) for t in l]
            
    else:
        return [TBA]


def _extractBrokenLoc(string):
    match = re.search("[A-Z]{2} [A-Z]*[0-9]+", string)
    if (match):
        return match.group(0)
    else:
        return "TBA"

def _extractBrokenTime(string):
    match = re.search("(M|T|W|R|F)+[0-9]+:*[0-9]*-*[0-9]*:*[0-9]* ?(\(p|A\))*", 
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
    
    