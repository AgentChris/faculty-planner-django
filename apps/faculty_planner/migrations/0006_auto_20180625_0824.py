# Generated by Django 2.0.6 on 2018-06-25 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('faculty_planner', '0005_yearstructure_faculty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='facebook_id',
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='faculty_planner.Specialization'),
        ),
    ]
