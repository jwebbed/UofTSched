import hashlib

_days = {'M' : 'Monday', 'T' : 'Tuesday', 'W': 'Wednesday', 'R' : 'Thursday',
         'F' : 'Friday'}


class Class:
    
    def __init__(this, code, sem, name):
        
        this.code = code
        this.sem = sem
        this.name = name
        this.lectures = []
        this.practicals - []
        this.tutorials = []
        
    def __str__(this):
        return this.code + " " + this.sem + " " + this.name
    
    def __repr__(this):
        return this.__str__()
    
    def addLec(this, lec):
        this.lectures.append(lec)
        
    def addPra(this, pra):
        this.praticals.append(pra)
    
    def addTut(this, tut):
        this.tutorials.append(tut)
    
    def verbose(this):
        s = str(this)
        for l in this.lectures:
            s += "\n\t" + str(l)
        for t in this.tutorials:
            s += "\n\t" + str(t)
        return s
    
    def getLectureTimeSlots(this):
        slots = []
        for slot in this.lectures:
            slots += slot.getTimeSlots()
        return slots
    
    def getPracticalTimeSlots(this):
            slots = []
            for slot in this.lectures:
                slots += slot.getTimeSlots()
            return slots    
    
    def getTutorialTimeSlots(this):
        
        return [slot.getTimeSlots for slot in this.tutorials]
       
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
        
    def getTimeSlots(this):
        
        return this.time
        
class PracticalSection:
    
    def __init__(this, code, instruct, alt = False):
        
        this.code = code
        this.instruct = instruct
        this.time = []
        this.alternating = alt
                

    def __str__(this):
        s = this.code + " " + this.instruct
        if (this.time != []):
            for i in this.time:
                s+= "\n\t\t" + str(i)
        
        return s
    
    def addTime(this, timeslot):
        this.time.append(timeslot) 
        
    def getTimeSlots(this):
        
        return this.time

class TutorialSection:
    
    def __init__(this, code, timeslot):
        
        this.code = code
        this.timeslot = timeslot
        
        
    def __str__(this):

        return this.code + " " + str(this.timeslot)
    
    def getTimeSlots(this):
        
        return this.timeslot

class TimeSlot:
    
    def __init__(this, *args):
        ''' Input should be day, location, start time and end time in this 
        order, otherwise only input should be None indicating TBA'''
        
        if (args[0] == None):
            this.TBA = True
            this.ID = 'TBA'
        else:
            this.day = args[0]
            this.loc = args[1]
            this.start = args[2]
            this.end = args[3]
            this.code = args[4]
            this.course = args[5]
            this.TBA = False
            this.__hash__()
     
    def time(this):
        ''' (TimeSlot) -> str
        Returns a string representing the time the class ocours at '''
    
        hour_start = this.start // 4
        minute_start = (this.start % 4) * 15
        hour_end = this.end // 4
        minute_end = (this.end % 4) * 15
        return "%02d:%02d-%02d:%02d" % (hour_start, minute_start,
                                                    hour_end, minute_end)        

    def __str__(this):
        if (this.TBA):
            return "TBA"
        else:
            
            return _days[this.day] + ' ' + this.loc + ' ' + this.time()
       
    def __repr__(this):
        return this.__str__()
        
    def __hash__(this):
        ''' Used to make a unique ID for this TimeSlot '''
        
        s = this.course.verbose()
        s += str(this.day)
        s += str(this.start)
        s += str(this.end)
        s += this.code
        b = str.encode(s)
        this.ID = hashlib.sha256(b).hexdigest()
        
    def __eq__(this, other):
        ''' (TimeSlot, TimeSlot) -> bool
        Returns True iff both time slots overlap for at least some ammount of 
        time, use the equals method if you want to know if they cover the exact
        same ammount of time '''
        
        return not (other.start >= this.end or other.end <= this.start)
    
    def equals(this, other):
        ''' (TimeSlot, TimeSlot) -> bool
        Returns true iff both time slots cover the exact same time '''
        
        return (other.start == this.start and other.end == this.end)
            
class TimeTable:
    
    def __init__(this):
        
        this.time_slots = []
        this.classes = []
        
    def addTimeSlot(this, slot):
        
        this.time_slots.append(slot)
        if (not (slot.course in this.classes)):
            this.classes.append(slot.course)
            
    def classList(this):
        ''' (TimeTable) -> str
        Returns a string of a list of classes in this time table '''
        
        s = ''
        for i in this.classes:
            s += str(i)
        return s
        
        
TBA = TimeSlot(None)