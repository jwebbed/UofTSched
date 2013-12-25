# Run this code in a `python manage.py shell`

from uoftsched.models import *
from datetime import time
t = TimeSlot(location='BA1170', weekday=2, start_time=time(2), end_time=time(3))
t.save()
c = Course(code="CSC108", semester="F", name="Intro")
c.save()
c.lecturesection_set.create(code="L0101", instructor="Jen Campbell", time=t)
c.save()
print(repr(c.lecturesection_set.first().time))