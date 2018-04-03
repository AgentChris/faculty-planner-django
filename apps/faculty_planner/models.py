import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Course(models.Model):
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.TextField(max_length=256)
    description = models.TextField(max_length=512)
    location = models.TextField(max_length=512)
    updated = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s ...' % (self.name[:32],)


class Professor(models.Model):
    class Meta:
        verbose_name = _('Professor')
        verbose_name_plural = _('Professor')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.TextField(max_length=256)
    email = models.CharField(max_length=128)
    updated = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s ...' % (self.name[:32],)


class Room(models.Model):
    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=128)
    location = models.TextField(max_length=512)  # google maps url


class Group(models.Model):
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    name = models.CharField(max_length=128)
    sub_group = models.DecimalField(max_digits=1)


class CourseDate(models.Model):
    class Meta:
        verbose_name = _('Course Date')
        verbose_name_plural = _('Course Dates')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    course = models.ForeignKey(Course)
    room = models.ForeignKey(Room)
    group = models.ForeignKey(Group)
    professor = models.ForeignKey(Professor)
    date = models.DateField(default=timezone.now)
    startHour = models.TimeField(default=timezone.now)
    endHour = models.TimeField(default=timezone.now)
    updated = models.DateField(default=timezone.now)


class Faculty(models.Model):
    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=128)


class Language(models.Model):
    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=256)


class Specialization(models.Model):
    class Meta:
        verbose_name = _('Specialization')
        verbose_name_plural = _('Specializations')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    faculty = models.ForeignKey(Faculty)
    group = models.ManyToManyField(Group, through="SpecializationGroup")
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=256)
    degree = models.CharField(max_length=128)
    frequency = models.CharField(max_length=128)
    year = models.DecimalField(max_digits=1)
    sem = models.DecimalField(max_digits=1)


class SpecializationGroup(models.Model):
    specialization = models.ForeignKey(Specialization)
    group = models.ForeignKey(Group)


class Student(models.Model):
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.TextField(max_length=256)
    email = models.CharField(max_length=128)
    specializations = models.ManyToManyField(Specialization, through='StudentSpecialization')


class Schedule(models.Model):
    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    course_date = models.ForeignKey(CourseDate)
    student = models.ForeignKey(Student)


class StudentSuggestion(models.Model):
    class Meta:
        verbose_name = _('Student Suggestion')
        verbose_name_plural = _('Student Suggestions')

    name = models.CharField(max_length=256)
    specialization_group = models.ForeignKey(SpecializationGroup)
    student = models.ForeignKey(Student, blank=True, null=True)


class StudentSpecialization(models.Model):
    class Meta:
        verbose_name = _('Student Specialization')
        verbose_name_plural = _('Student Specializations')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    student = models.ForeignKey(Student)
    specialization = models.ForeignKey(Specialization)
