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
    
    def __init__(this, code, instruct):
        
        this.code = code
        this.instruct = instruct
        this.time = []
                

    def __str__(this):
        s = this.code + " " + this.instruct
        if (this.time != []):
            for i in this.time:
                s+= "\n\t\t" + str(i)
        
        return s
    
    def addTime(this, timeslot):
        this.time.append(timeslot)       
        

class TutorialSection:
    
    def __init__(this, code, timeslot):
        
        this.code = code
        this.timeslot = timeslot
        
        
    def __str__(this):

        return "BLAH"

class TimeSlot:
    
    def __init__(this, *args):
        ''' Input should be day, location, start time and end time in this 
        order, otherwise only input should be None indicating TBA'''
        
        if (args[0] == None):
            this.TBA = True           
        else:
            this.day = args[0]
            this.loc = args[1]
            this.start = args[2]
            this.end = args[3]
            this.TBA = False
        
    def __str__(this):
        if (this.TBA):
            return "TBA"
        else:
            return (_days[this.day] + ' ' + this.loc + ' ' + str(this.start) 
                    + '-' + str(this.end))

        
TBA = TimeSlot(None)