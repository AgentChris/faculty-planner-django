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
    sub_group = models.DecimalField(max_digits=1, decimal_places=1)


class CourseDate(models.Model):
    MONDAY = 'MON'
    TUESDAY = 'TUES'
    WEDNESDAY = 'WED'
    THURSDAY = 'THURS'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'
    DAY_IN_WEEK = (
        (MONDAY, 'MONDAY'),
        (TUESDAY, 'TUESDAY'),
        (WEDNESDAY, 'WEDNESDAY'),
        (THURSDAY, 'THURSDAY'),
        (FRIDAY, 'FRIDAY'),
        (SATURDAY, 'SATURDAY'),
        (SUNDAY, 'SUNDAY'),
    )
    ODD = 'O'
    EVEN = 'E'
    EVERY_WEEK = 'W'
    PARITY = (
        (ODD, 'OOD'),
        (EVEN, 'EVEN'),
        (EVERY_WEEK, 'EVERY_WEEK'),
    )

    class Meta:
        verbose_name = _('Course Date')
        verbose_name_plural = _('Course Dates')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    course = models.ForeignKey(Course)
    parity_week = models.CharField(max_length=1, choices=PARITY, default=EVERY_WEEK)
    room = models.ForeignKey(Room)
    group = models.ForeignKey(Group)
    professor = models.ForeignKey(Professor)
    day_in_week = models.CharField(max_length=5, choices=DAY_IN_WEEK, default=None)
    start_hour = models.TimeField(default=timezone.now)
    end_hour = models.TimeField(default=timezone.now)
    updated = models.DateField(default=timezone.now)


class Faculty(models.Model):
    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=128)
    link = models.CharField(max_length=512)


class Language(models.Model):
    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=256)


class Specialization(models.Model):
    BACHELOR = 'BACHELOR'
    MASTER = 'MASTER'
    DOCTORAL = 'DOCTORAL'
    DEGREE = (
        (BACHELOR, 'BACHELOR'),
        (MASTER, 'MASTER'),
        (DOCTORAL, 'DOCTORAL'),
    )

    class Meta:
        verbose_name = _('Specialization')
        verbose_name_plural = _('Specializations')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    faculty = models.ForeignKey(Faculty)
    group = models.ForeignKey(Group)
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=256)
    degree = models.CharField(max_length=50, choices=DEGREE, default=BACHELOR)
    with_frequency = models.BooleanField(default=True)
    year = models.DecimalField(max_digits=1, decimal_places=1)
    sem = models.DecimalField(max_digits=1, decimal_places=1)


class SpecializationGroup(models.Model):
    specialization = models.ForeignKey(Specialization)
    group = models.ForeignKey(Group)


class Student(models.Model):
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    facebook_id = models.TextField(max_length=256)
    name = models.TextField(max_length=256)
    email = models.EmailField(max_length=256)
    specializations = models.ManyToManyField(Specialization, through='StudentSpecialization')


class Schedule(models.Model):
    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    specialization = models.ForeignKey(Specialization)


class ScheduleCourseDate(models.Model):
    course_date = models.ForeignKey(CourseDate)
    schedule = models.ForeignKey(Schedule)


class StudentSuggestion(models.Model):
    class Meta:
        verbose_name = _('Student Suggestion')
        verbose_name_plural = _('Student Suggestions')

    name = models.CharField(max_length=256)
    specialization_group = models.ForeignKey(SpecializationGroup)


class StudentSpecialization(models.Model):
    class Meta:
        verbose_name = _('Student Specialization')
        verbose_name_plural = _('Student Specializations')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    student = models.ForeignKey(Student)
    specialization = models.ForeignKey(Specialization)
