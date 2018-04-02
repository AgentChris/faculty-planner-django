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


class CourseDate(models.Model):
    class Meta:
        verbose_name = _('Course Date')
        verbose_name_plural = _('Course Dates')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    course = models.ForeignKey(Course)
    professor = models.ForeignKey(Professor)
    date = models.DateField(default=timezone.now)
    updated = models.DateField(default=timezone.now)


class Faculty(models.Model):
    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.CharField(max_length=128)


class Specialization(models.Model):
    class Meta:
        verbose_name = _('Specialization')
        verbose_name_plural = _('Specialization')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    faculty = models.ForeignKey(Faculty)
    # TODO ADD year specialization language master or licenta


class Student(models.Model):
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    name = models.TextField(max_length=256)
    email = models.CharField(max_length=128)
    specializations = models.ManyToManyField(Specialization, through='StudentSpecialization')


class StudentSpecialization(models.Model):
    class Meta:
        verbose_name = _('Student Specialization')
        verbose_name_plural = _('Student Specializations')

    uuid = models.CharField(default=uuid.uuid4, null=True, max_length=256)
    student = models.ForeignKey(Student)
    specialization = models.ForeignKey(Specialization)
