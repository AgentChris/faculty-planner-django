import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

COURSE = 'C'
SEMINAR = 'S'
LABORATORY = 'L'
COURSE_TYPE = (
    (COURSE, 'COURSE'),
    (SEMINAR, 'SEMINAR'),
    (LABORATORY, 'LABORATORY'),
)


class Course(models.Model):
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.TextField(max_length=256)
    c_type = models.CharField(max_length=1, choices=COURSE_TYPE, default=COURSE)
    description = models.TextField(max_length=512)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '%s... %s' % (self.name[:52], self.c_type)


class Professor(models.Model):
    class Meta:
        verbose_name = _('Professor')
        verbose_name_plural = _('Professor')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.TextField(max_length=256)
    link = models.TextField(max_length=256, default="")
    email = models.CharField(max_length=128, null=True, default="")
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name,)


class Room(models.Model):
    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=128)
    location = models.TextField(max_length=512)  # google maps url

    def __str__(self):
        return self.name


class Group(models.Model):
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    name = models.CharField(max_length=128)
    sub_group = models.IntegerField()

    def __str__(self):
        return '%s - sg%s' % (self.name, self.sub_group)


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


class CourseDate(models.Model):
    class Meta:
        verbose_name = _('Course Date')
        verbose_name_plural = _('Course Dates')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    course = models.ForeignKey(Course)
    parity_week = models.CharField(max_length=1, choices=PARITY, default=EVERY_WEEK)
    extra_info = models.CharField(max_length=128, default="")
    room = models.ForeignKey(Room)
    groups = models.ManyToManyField(Group, through='CourseDateGroup')
    professor = models.ForeignKey(Professor)
    day_in_week = models.CharField(max_length=5, choices=DAY_IN_WEEK, default=None)
    start_hour = models.TimeField(null=True)
    end_hour = models.TimeField(null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '%s... - room %s - prof. %s %s %s:%s - %s:%s' \
               % (self.course.name[:32], self.room.name, self.professor.name, self.day_in_week,
                  self.start_hour.hour, self.start_hour.minute, self.end_hour.hour, self.end_hour.minute)


class CourseDateGroup(models.Model):
    class Meta:
        verbose_name = _('Course Date')
        verbose_name_plural = _('Course Dates')

    course_date = models.ForeignKey(CourseDate)
    group = models.ForeignKey(Group)


class Faculty(models.Model):
    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=128)
    link = models.CharField(max_length=512)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name,)


class Language(models.Model):
    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=256)

    def __str__(self):
        return '%s' % (self.name,)


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
    groups = models.ManyToManyField(Group, through='SpecializationGroup')
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=256)
    link = models.CharField(max_length=512)
    acronym = models.CharField(max_length=128)
    degree = models.CharField(max_length=50, choices=DEGREE, default=BACHELOR)
    with_frequency = models.BooleanField(default=True)
    year = models.IntegerField()
    sem = models.IntegerField()
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '%s... - year %s - sem %s - %s - %s - %s' \
               % (self.name[:32], self.year, self.sem, self.language,
                  self.degree, self.faculty.acronym)


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
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    specializations = models.ManyToManyField(Specialization, through='StudentSpecialization')


class Schedule(models.Model):
    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    specialization = models.ForeignKey(Specialization, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    course_dates = models.ManyToManyField(CourseDate, through='ScheduleCourseDate')


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
