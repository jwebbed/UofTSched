from time_date_objects import *
import hashlib

_days = {'M' : Monday(), 'T' : Tuesday(), 'W': Wednesday(), 'R' : Thursday(),
         'F' : Friday(), 'S' : Saturday(), 'N' : Sunday()}


class Course: ## NYI
    
    def __init__(self, **kwargs):
        '''
        
        :kwargs:
        timeslots - A list of TimeSlot objects
        
        '''
        pass
    
    
class TimeSlot: ## NYI
    
    def __init__(this, **kwargs):
        '''
        :kwargs:
        course - The course this timeslot belongs to
        '''
        
        this.course = None
        
    
    def isValid(this):
        if (type(this.course) == Course):
            return True

        
        
        