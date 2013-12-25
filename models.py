from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=10)
    semester = models.CharField(max_length=1)
    name = models.CharField(max_length=50)


    def __init__(self, code, sem, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

class Section(models.Model):
    course = models.ForeignKey(Course)
    pass

class LectureSection(Section):
    pass

class TutorialSection(Section):
    pass

class PracticalSection(Section):
    pass

