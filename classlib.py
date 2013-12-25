import hashlib

_days = {'M' : 'Monday', 'T' : 'Tuesday', 'W': 'Wednesday', 'R' : 'Thursday',
         'F' : 'Friday'}


class Class:
    
    def __init__(self, code, sem, name):
        
        self.code = code
        self.sem = sem
        self.name = name
        self.lectures = []
        self.practicals = []
        self.tutorials = []
        
    def __str__(self):
        return self.code + " " + self.sem + " " + self.name
    
    def __repr__(self):
        return self.__str__()
    
    def addLec(self, lec):
        self.lectures.append(lec)
        
    def addPra(self, pra):
        self.practicals.append(pra)
    
    def addTut(self, tut):
        self.tutorials.append(tut)
    
    def verbose(self):
        s = str(self)
        for l in self.lectures:
            s += "\n\t" + str(l)
        for t in self.tutorials:
            s += "\n\t" + str(t)
        return s
    
    def getLectureTimeSlots(self):
        slots = []
        for slot in self.lectures:
            slots += slot.getTimeSlots()
        return slots
    
    def getPracticalTimeSlots(self):
            slots = []
            for slot in self.practicals:
                slots += slot.getTimeSlots()
            return slots    
    
    def getTutorialTimeSlots(self):
        
        return [slot.getTimeSlots for slot in self.tutorials]
    
    def getTimeSlots(self):
        
        l = []
        lec = self.getLectureTimeSlots()
        pra = self.getPracticalTimeSlots()
        tut = self.getTutorialTimeSlots()
        
        if (len(lec) != 0):
            l.append(lec)
        if (len(pra) != 0):
            l.append(pra)
        if (len(tut) != 0):
            l.append(tut)  
            
        return l
    
    def getSections(self):
            
        l = []
        if (len(self.lectures) != 0):
            l.append(self.lectures)
        if (len(self.practicals) != 0):
            l.append(self.practicals)
        if (len(self.tutorials) != 0):
            l.append(tut)  
            
        return l 
        
    def TBA(self):
        ''' Returns true if anything in this class is TBA '''
        for l in self.getTimeSlots():
            if (TBA in l):
                return True
        return False
        
class LectureSection:
    
    def __init__(self, code, instruct):
        
        self.code = code
        self.instruct = instruct
        self.time = []
                

    def __str__(self):
        s = self.code + " " + self.instruct
        if (self.time != []):
            for i in self.time:
                s+= "\n\t\t" + str(i)
        
        return s
    
    def addTime(self, timeslot):
        self.time.append(timeslot)
        
    def getTimeSlots(self):
        
        return self.time
        
class PracticalSection:
    
    def __init__(self, code, instruct, alt = False):
        
        self.code = code
        self.instruct = instruct
        self.time = []
        self.alternating = alt
                

    def __str__(self):
        s = self.code + " " + self.instruct
        if (self.time != []):
            for i in self.time:
                s+= "\n\t\t" + str(i)
        
        return s
    
    def addTime(self, timeslot):
        self.time.append(timeslot)
        
    def getTimeSlots(self):
        
        return self.time

class TutorialSection:
    
    def __init__(self, code, timeslot):
        
        self.code = code
        self.timeslot = timeslot
        
        
    def __str__(self):

        return self.code + " " + str(self.timeslot)
    
    def getTimeSlots(self):
        
        return self.timeslot

class TimeSlot:
    
    def __init__(self, *args):
        ''' Input should be day, location, start time and end time in this
        order, otherwise only input should be None indicating TBA'''
        
        if (args[0] == None):
            self.TBA = True
            self.ID = b'TBA'
        else:
            self.day = args[0]
            self.loc = args[1]
            self.start = args[2]
            self.end = args[3]
            self.TBA = False
            self.code = args[4]
            self.course = args[5]
            self.__hash__()
     
    def time(self):
        ''' (TimeSlot) -> str
        Returns a string representing the time the class ocours at '''
    
        hour_start = self.start // 4
        minute_start = (self.start % 4) * 15
        hour_end = self.end // 4
        minute_end = (self.end % 4) * 15
        return "%02d:%02d-%02d:%02d" % (hour_start, minute_start,
                                                    hour_end, minute_end)        

    def __str__(self):
        if (self.TBA):
            return "TBA"
        else:
            
            return _days[self.day] + ' ' + self.loc + ' ' + self.time()
       
    def __repr__(self):
        return self.__str__()
        
    def __hash__(self):
        ''' Used to make a unique ID for this TimeSlot '''
        
        s = self.course.code
        s += str(self.day)
        s += str(self.start)
        s += str(self.end)
        s += self.code
        b = str.encode(s)
        self.ID = hashlib.sha256(b).hexdigest()
        
    def __eq__(self, other):
        ''' (TimeSlot, TimeSlot) -> bool
        Returns True iff both time slots overlap for at least some ammount of 
        time, use the equals method if you want to know if they cover the exact
        same ammount of time '''
        
        if (type(other) != type(self) or self is TBA or other is TBA or
            (self.sem == 'F' and other.sem == 'S')):
            return False
        else:
            return ((not (other.end <= self.start or other.start >= self.end))
                    and self.day == other.day)
    
    def equals(self, other):
        ''' (TimeSlot, TimeSlot) -> bool
        Returns true iff both time slots cover the exact same time '''
        
        return (other.start == self.start and other.end == self.end)
            
class TimeTable:
    
    def __init__(self):
        
        self.time_slots = []
        self.classes = []
        
    def addTimeSlot(self, slot):
        
        self.time_slots.append(slot)
        if (not (slot.course in self.classes)):
            self.classes.append(slot.course)
            
    def classList(self):
        ''' (TimeTable) -> str
        Returns a string of a list of classes in this time table '''
        
        s = ''
        for i in self.classes:
            s += str(i) + '\n'
        return s
    
    def conflict(self):
        ''' (TimeTable) -> bool
        Returns true iff any of the time slots in this timeable are
        conflicting'''
        
        if (len(self.time_slots) < 2):
            return False
        else:
            for i in range(len(self.time_slots) - 1):
                for slot in self.time_slots[i + 1:]:
                    if (slot == self.time_slots[i]):
                        return True
        return False
                    
                    
                    
TBA = TimeSlot(None)
