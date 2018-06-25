from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Specialization, Group, Faculty, Language, \
    CourseDate, Course, Room, Professor, DayType, Student


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('uuid', 'name', 'sub_group')


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('uuid', 'name', 'acronym', 'link')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('uuid', 'name')


class SpecializationSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    faculty = FacultySerializer(many=False)
    language = LanguageSerializer(many=False)

    # TODO maybe with orar link
    class Meta:
        model = Specialization
        fields = ('uuid', 'name', 'acronym', 'degree', 'faculty',
                  'year', 'sem', 'language', 'groups', 'with_frequency',)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('uuid', 'name', 'c_type', 'description')


class ProfessorSerializer(serializers.ModelSerializer):
    # TODO maybe add professor link and email
    class Meta:
        model = Professor
        fields = ('uuid', 'name')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('uuid', 'name', 'location')


class CourseDateSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False)
    professor = ProfessorSerializer(many=False)
    room = RoomSerializer(many=False)

    # TODO maybe add groups to field
    class Meta:
        model = CourseDate
        fields = ('uuid', 'room', 'course', 'parity_week', 'professor',
                  'extra_info', 'day_in_week', 'start_hour', 'end_hour')


class DayTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayType
        fields = ('uuid', 'type', 'detail', 'start_date', 'end_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    specializations = SpecializationSerializer(many=True)
    # user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = ('name', 'email', 'specializations')
