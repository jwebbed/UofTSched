from classlib import *
from bs4 import BeautifulSoup
import requests
import re
import math
import traceback
import sys

def WebCrawler():
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
                    
                    code = str(col[0].string)
                    sem = str(col[1].string)
                    if (sem == 'None'):
                        if (re.search('S', str(col[1]))):
                            sem = 'S'
                        elif (re.search('Y', str(col[1]))):
                            sem = 'Y'
                        elif (re.search('F', str(col[1]))):
                            sem = 'F'
                        else:
                            print("Course Code: " + code)
                            print("HTML Code: " + str(col[1]))
                            sem = input("What is the sem?")
                            if (sem != 'S' or sem != 'F' or sem != 'Y'):
                                raise NoSemesterException(code, str(col[1]))
                    name = str(col[2].string)
                    if (not re.match("[a-zA-Z\s]*", name)):
                        name = _extractBroken(name)     
                    curr = Class(code, sem, name)
                    class_list.append(curr)
                
                if (re.search('L[0-9]{4}', str(col[3]))):        
                    if (col[3].string != None):
                        code = str(col[3].string) 
                    else:
                        code = _extractBrokenCode(str(col[3]))
                                                  
                    if (col[5].string != None):
                        time = str(col[5].string)
                    else:
                        x = str(col[5].strong)
                        time = _extractBrokenTime(str(col[5]))
                        
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
                    for slot in _generateTimeSlot(time, loc, code, curr):
                        sec.addTime(slot)
                    curr.addLec(sec)
                elif (re.search('P[0-9]{4}', str(col[3]))):
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
                    for slot in _generateTimeSlot(time, loc, code, curr):
                        sec.addTime(slot)
                    curr.addLec(sec)                
                elif (re.search('T[0-9]{4}', str(col[3]))):
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
                        
                    curr.addTut(TutorialSection(
                        code, _generateTimeSlot(time, loc, code, curr)[0]))
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
                    for slot in _generateTimeSlot(time, loc, code, curr):
                        sec.addTime(slot)   
    
    except NoSemesterException as e:
        print("No Valid Semester Found")
        print("Course Code: " + e.course)
        print(e.code)
        
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
            
    return class_list
   

def _generateTimeSlot(time, loc, course_code, course_obj):
    if (time != "TBA"):
        l, s, start, end = [], '', None, None
        

        for char in time:
            if (re.match("(M|T|W|R|F)", char)):
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
        else:
            raise Exception("Unable to read time format")
        
        if (start and end):
            return [TimeSlot(t, loc, start, end, course_code, course_obj) 
                    for t in l]
        else:
            return [TBA]
            
    else:
        return [TBA]


def _extractBrokenLoc(string):
    match = re.search("[A-Z]{2} [A-Z]*[0-9]+", string)
    if (match):
        return match.group(0)
    elif (re.search("GI", string)):
        return "GI"
    elif (re.search("[A-Za-z ]*", string)):
        match = re.search("[A-Za-z ]*", string)
        return match.group(0)
    else:
        raise Exception("Unable to extract broken Location Format")
    
def _extractBrokenTime(string):
    match = re.search("(M|T|W|R|F)+[0-9]+:*[0-9]*-*[0-9]*:*[0-9]*", 
                      string)
    if (match):
        return match.group(0)
    else:
        raise Exception("Unable to extract broken Location Format")

def _extractBrokenCode(string):
    match = re.search("(L|T|P)[0-9]{4}", string)
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

## Exceptions ##

class CrawlerError(Exception):
    def __init__(this, course, code):
        this.course = course
        this.code = code    
    
class NoSemesterException(CrawlerError):
    pass
    
if __name__ == "__main__":
    x = WebCrawler()
    s = ''
    for i in x:
        s += i.verbose() + '\n'
    f = open('downloaded_data.txt', 'w')
    f.write(s)
    f.close()
    
    
    