# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-08 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('name', models.TextField(max_length=256)),
                ('c_type', models.CharField(choices=[('C', 'COURSE'), ('S', 'SEMINAR'), ('L', 'LABORATORY')], default='C', max_length=1)),
                ('description', models.TextField(max_length=512)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('parity_week', models.CharField(choices=[('O', 'OOD'), ('E', 'EVEN'), ('W', 'EVERY_WEEK')], default='W', max_length=1)),
                ('extra_info', models.CharField(default='', max_length=128)),
                ('day_in_week', models.CharField(choices=[('MON', 'MONDAY'), ('TUES', 'TUESDAY'), ('WED', 'WEDNESDAY'), ('THURS', 'THURSDAY'), ('FRI', 'FRIDAY'), ('SAT', 'SATURDAY'), ('SUN', 'SUNDAY')], default=None, max_length=5)),
                ('start_hour', models.DateTimeField(null=True)),
                ('end_hour', models.DateTimeField(null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Course')),
            ],
            options={
                'verbose_name': 'Course Date',
                'verbose_name_plural': 'Course Dates',
            },
        ),
        migrations.CreateModel(
            name='CourseDateGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.CourseDate')),
            ],
            options={
                'verbose_name': 'Course Date',
                'verbose_name_plural': 'Course Dates',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('name', models.CharField(max_length=128)),
                ('acronym', models.CharField(max_length=128)),
                ('link', models.CharField(max_length=512)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('sub_group', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('name', models.TextField(max_length=256)),
                ('link', models.TextField(default='', max_length=256)),
                ('email', models.CharField(default='', max_length=128, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Professor',
                'verbose_name_plural': 'Professor',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('name', models.CharField(max_length=128)),
                ('location', models.TextField(max_length=512)),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
            },
        ),
        migrations.CreateModel(
            name='ScheduleCourseDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.CourseDate')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('name', models.CharField(max_length=256)),
                ('link', models.CharField(max_length=512)),
                ('acronym', models.CharField(max_length=128)),
                ('degree', models.CharField(choices=[('BACHELOR', 'BACHELOR'), ('MASTER', 'MASTER'), ('DOCTORAL', 'DOCTORAL')], default='BACHELOR', max_length=50)),
                ('with_frequency', models.BooleanField(default=True)),
                ('year', models.IntegerField()),
                ('sem', models.IntegerField()),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Faculty')),
            ],
            options={
                'verbose_name': 'Specialization',
                'verbose_name_plural': 'Specializations',
            },
        ),
        migrations.CreateModel(
            name='SpecializationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Group')),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Specialization')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('facebook_id', models.TextField(max_length=256)),
                ('name', models.TextField(max_length=256)),
                ('email', models.EmailField(max_length=256)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='StudentSpecialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=256, null=True)),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Specialization')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Student')),
            ],
            options={
                'verbose_name': 'Student Specialization',
                'verbose_name_plural': 'Student Specializations',
            },
        ),
        migrations.CreateModel(
            name='StudentSuggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('specialization_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.SpecializationGroup')),
            ],
            options={
                'verbose_name': 'Student Suggestion',
                'verbose_name_plural': 'Student Suggestions',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='specializations',
            field=models.ManyToManyField(through='faculty_planner.StudentSpecialization', to='faculty_planner.Specialization'),
        ),
        migrations.AddField(
            model_name='specialization',
            name='groups',
            field=models.ManyToManyField(through='faculty_planner.SpecializationGroup', to='faculty_planner.Group'),
        ),
        migrations.AddField(
            model_name='specialization',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Language'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='course_dates',
            field=models.ManyToManyField(through='faculty_planner.ScheduleCourseDate', to='faculty_planner.CourseDate'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Specialization'),
        ),
        migrations.AddField(
            model_name='coursedategroup',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Group'),
        ),
        migrations.AddField(
            model_name='coursedate',
            name='groups',
            field=models.ManyToManyField(through='faculty_planner.CourseDateGroup', to='faculty_planner.Group'),
        ),
        migrations.AddField(
            model_name='coursedate',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Professor'),
        ),
        migrations.AddField(
            model_name='coursedate',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Room'),
        ),
    ]
