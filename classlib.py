import re

_days = {'M' : 'Monday', 'T' : 'Tuesday', 'W': 'Wednesday', 'R' : 'Thursday',
         'F' : 'Friday'}


class Class:
    
    def __init__(this, code, sem, name):
        
        this.code = code
        this.sem = sem
        this.name = name
        this.lectures = []
        this.tutorials = []
        
    def __str__(this):
        return this.code + " " + this.sem + " " + this.name
    
    def addLec(this, lec):
        this.lectures.append(lec)
    
    def addTut(this, tut):
        this.tutorials.append(tut)
    
    def verbose(this):
        s = str(this)
        for l in this.lectures:
            s += "\n\t" + str(l)
        for t in this.tutorials:
            s += "\n\t" + str(t)
        return s
        
class LectureSection:
    
    def __init__(this, code, time, loc, instruct):
        
        this.code = code
        this.instruct = instruct
        this.time = []
        
        if (time == "TBA"):
            return
        
        l = []
        s = ''
        for char in time:
            if (re.match("[A-Z]", char)):
                l.append(char)
            else:
                s += char
        
        for t in l:
            this.time.append(TimeSlot(t, loc, int(s[0]), int(s[-1])))
                

    def __str__(this):
        s = this.code + " " + this.instruct
        if (this.time != []):
            for i in this.time:
                s+= "\n\t\t" + str(i)
        
        return s
    
    def addTime(this, time, loc):
        if (time == "TBA"):
            return
                
        l = []
        s = ''
        for char in time:
            if (re.match("[A-Z]", char)):
                l.append(char)
            else:
                s += char
                
        for t in l:
            this.time.append(TimeSlot(t, loc, int(s[0]), int(s[-1])))        
        

class TutorialSection:
    
    def __init__(this, code, time, loc):
        
        this.code = code
        this.day = _days[time[0]]
        this.time = time[1:]
        this.loc = loc 
        
    def __str__(this):
        
        return this.code + " " + this.day + " " + this.time + " " + this.loc

class TimeSlot:
    
    def __init__(this, day, loc, start, end):
        this.day = day
        this.loc = loc
        this.start = start
        this.end = end
        
    def __str__(this):
        return (_days[this.day] + ' ' + this.loc + ' ' + str(this.start) + '-' +
                str(this.end))