from django.db import models


class Course(models.Model):
    """
    A course.
    """

    code = models.CharField(max_length=10)
    semester = models.CharField(max_length=1)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code + self.semester


class TimeSlot(models.Model):
    """
    A weekday and time for a course meeting.
    """

    _DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    location = models.CharField(max_length=10)
    tba = models.BooleanField(default=False)
    weekday = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        if self.tba:
            return "TBA"
        else:
            time = "{:%I:%M}-{:%I:%M}".format(self.start_time, self.end_time)
            return TimeSlot._DAYS[self.weekday] + ' ' + time


class Section(models.Model):
    """
    Abstract class for meeting sections.
    """

    course = models.ForeignKey(Course)
    code = models.CharField(max_length=10)
    instructor = models.CharField(max_length=50)
    time = models.OneToOneField(TimeSlot)

    class Meta:
        abstract = True

    def __str__(self):
        return self.code


class LectureSection(Section):
    """
    A lecture section.
    """

    pass


class TutorialSection(Section):
    """
    A tutorial section
    """

    pass


class PracticalSection(Section):
    """
    A practical section.
    """

    pass
