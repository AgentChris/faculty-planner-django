from rest_framework import serializers

from .models import Specialization, Group, Faculty, Language, \
    CourseDate


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

    class Meta:
        model = Specialization
        fields = ('uuid', 'name', 'acronym', 'degree', 'faculty',
                  'year', 'sem', 'language', 'groups', 'with_frequency',)


class CourseDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDate
        fields = ('uuid',)
