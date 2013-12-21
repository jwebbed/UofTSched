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
        this.day = _days[time[0]]
        this.time = time[1:]
        this.loc = loc
        this.instruct = instruct

    def __str__(this):
        
        return (this.code + " " + this.day + " " + this.time + " " +
                this.loc + " " + this.instruct)
    
class TutorialSection:
    
    def __init__(this, code, time, loc):
        
        this.code = code
        this.day = _days[time[0]]
        this.time = time[1:]
        this.loc = loc 
        
    def __str__(this):
        
        return this.code + " " + this.day + " " + this.time + " " + this.loc