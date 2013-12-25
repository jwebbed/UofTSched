from classlib import *
from WebCrawler import WebCrawler

def generateTimeTables(classes):
    ##Do Something
    pass

def _allPossibleTimeTables(classes, conflict = False):
    ''' (List of Class, bool) -> List of TimeTable
    Returns a list of all possible TimeTables from the given classes. If
    conflict is True then this will include TimeTables with conflict, otherwise
    it will not '''
    
    l = []
    for i in classes:
        l += i.getTimeSlots()
    
    timetables = [_makeTimeTable(subset) for subset in _listSubsetter(l)]
    
    if (not conflict):
        for timetable in timetables:
            if (timetable.conflict()):
                timetables.remove(timetable)
    
    return timetables

def _makeTimeTable(slots):
    ''' (List of TimeSlot) -> TimeTable
    Takes a list of TimeSlot objects and returns a TimeTable object '''
    
    tt = TimeTable()
    for slot in slots:
        tt.addTimeSlot(slot)
    return tt

def _listSubsetter(l):
    ''' (List of List of obj) -> List of list of obj
    Returns a list of all the combinations that can be made with replacement
    by taking one object from each list in the list  '''
    
    if (len(l) == 1):
        return [[i] for i in l[0]]
    
    partial = _listSubsetter(l[1:])
    new = []
    for item in l[0]:
        for lst in partial:
            new.append(lst + [item])
            
    return new

courses = WebCrawler()