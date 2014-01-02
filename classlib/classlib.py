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
        
class Time:
    
    def __init__(this, start, end, accuracy = 15):
        ''' (Time, int) -> Time
        Creates an instance of a Time Object. The accuracy is how often time
        segments are split up. Example: with accuracy 15 an hour would be split
        up into 4 segments of 15 minutes each. Ideally accuracy is the highest
        value possible for a given school, at UofT the largest ofset from the
        begining of the hour a class can start is 15 minutes so 15 is the
        default. The value also has to evenly divide into the number of minutes
        in a day which is to say that (24*60) % accuracy == 0 
        
        The start is an integer representing the start time and the end is an 
        integer represting the end time. The end is always larger than the start
        and they're both always less than (24*60)/accuracy. The integer is 
        basically the nth slice of the day, where the number of slices is
        dependant on the accuracy
        '''
        
        assert (1440 % accuracy == 0)
        this.slices = 1440 // accuracy
        this.accuracy = accuracy
        
        assert (start < end)
        assert ((start < this.slices) and (end < this.slices))
        this.start = start
        this.end = end
        
    def length(this):
        ''' (Time) -> int
        Returns the length of this Time object in minutes
        '''
        
        return (this.end - this.start) * this.accuracy
    
    def __str__(this):
        ''' (Time) -> str
        Returns a string representation of this Time object in 24 time
        '''
        start = this.start * this.accuracy
        start_hour = start // 60
        start_min = start % 60
        end = this.end * this.accuracy
        end_hour = end // 60
        end_min = end % 60
        
        start_str = str(start_hour) + ':'   + "{0:0=2d}".format(start_min)
        
        end_str = str(end_hour) + ':' + "{0:0=2d}".format(end_min)
        
        return start_str + ' - ' + end_str
        
        
        