import json

from django.http import JsonResponse

from .models import StudentSuggestion, Specialization, Student, \
    Schedule, CourseDate, YearStructure, Faculty
from .parse_fsega import get_specialization_website_url, add_professor_information
from .serializers import SpecializationSerializer, CourseDateSerializer, DayTypeSerializer
from .services import store_specialization


# from django.core.exceptions import ObjectDoesNotExist
# from django.shortcuts import render, redirect
# from django.urls import reverse

# from myngs.models import MyDashboardUserProfile


def scrape_faculty(request):
    get_specialization_website_url()
    return JsonResponse({}, safe=False)


def get_schedule_by_specialization_uuid(request, *args, **kwargs):
    specialization_uuid = request.GET.get('specialization_uuid')

    specialization = Specialization.objects.get(specialization_uuid=specialization_uuid)
    schedule = Schedule.objects.get(specialization=specialization)

    return JsonResponse(schedule, safe=False)


def create_student(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    name = body.get('name')
    email = body.get('email')
    facebook_id = body.get('facebook_id')

    Student.objects.create(name=name, email=email, facebook_id=facebook_id)


def store_student_specialization(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # TODO: get uuid from jwt token, and then remove the hardcoded uuid
    uuid = "12312"

    specialization_uuid = body.get('specialization_uuid')

    specialization = store_specialization(student_uuid=uuid, specialization_uuid=specialization_uuid)

    return JsonResponse(specialization, safe=False)


def get_schedule_by_group(request, *args, **kwargs):
    group_uuid_param = request.GET.get('group')

    course_date = CourseDate.objects.filter(groups__uuid__contains=group_uuid_param)
    course_date_serializer = CourseDateSerializer(course_date, many=True)

    return JsonResponse(course_date_serializer.data, safe=False)


def get_specializations(request, *args, **kwargs):
    faculty_param = request.GET.get('faculty')

    specializations = Specialization.objects.filter(faculty__acronym=faculty_param)
    specializations_serializer = SpecializationSerializer(specializations, many=True)

    return JsonResponse(specializations_serializer.data, safe=False)


def get_student_suggestion(request, *args, **kwargs):
    name_param = request.GET.get('name')

    student_suggestions = StudentSuggestion.objects.get(name=name_param)

    response = []

    for student_suggestion in student_suggestions:
        (specialization,) = student_suggestion
        response.append(specialization)

    return JsonResponse(response, safe=False)


def parse_professor_information(request, *args, **kwargs):
    add_professor_information()


def get_year_structures(request, *args, **kwargs):
    faculty_param = request.GET.get('faculty', 'FSEGA')
    year_param = request.GET.get('year', 1)
    sem_param = request.GET.get('sem', 1)
    final_param = request.GET.get('final')

    final = False
    if final_param == 'true':
        final = True

    faculty = Faculty.objects.get(acronym=faculty_param)
    year_structures = YearStructure.objects \
        .get(faculty=faculty, year=year_param, sem=sem_param, final_years=final)

    response = []

    if year_structures:
        for day in year_structures.days.all():
            day_serializer = DayTypeSerializer(day, many=False)
            response.append(day_serializer.data)

    return JsonResponse(response, safe=False)
