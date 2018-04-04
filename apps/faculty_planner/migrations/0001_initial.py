# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-04 22:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
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
                ('description', models.TextField(max_length=512)),
                ('location', models.TextField(max_length=512)),
                ('updated', models.DateField(default=django.utils.timezone.now)),
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
                ('day_in_week', models.CharField(choices=[('MON', 'MONDAY'), ('TUES', 'TUESDAY'), ('WED', 'WEDNESDAY'), ('THURS', 'THURSDAY'), ('FRI', 'FRIDAY'), ('SAT', 'SATURDAY'), ('SUN', 'SUNDAY')], default=None, max_length=5)),
                ('start_hour', models.TimeField(default=django.utils.timezone.now)),
                ('end_hour', models.TimeField(default=django.utils.timezone.now)),
                ('updated', models.DateField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Course')),
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
                ('sub_group', models.DecimalField(decimal_places=1, max_digits=1)),
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
                ('email', models.CharField(max_length=128)),
                ('updated', models.DateField(default=django.utils.timezone.now)),
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
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
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
                ('acronym', models.CharField(max_length=128)),
                ('degree', models.CharField(choices=[('BACHELOR', 'BACHELOR'), ('MASTER', 'MASTER'), ('DOCTORAL', 'DOCTORAL')], default='BACHELOR', max_length=50)),
                ('with_frequency', models.BooleanField(default=True)),
                ('year', models.DecimalField(decimal_places=1, max_digits=1)),
                ('sem', models.DecimalField(decimal_places=1, max_digits=1)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Faculty')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Group')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Language')),
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
            model_name='schedule',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Specialization'),
        ),
        migrations.AddField(
            model_name='coursedate',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_planner.Group'),
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
