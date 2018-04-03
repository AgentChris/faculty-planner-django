import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from faculty_planner import services
from .models import StudentSuggestion, Specialization, Student, Schedule


# from django.core.exceptions import ObjectDoesNotExist
# from django.shortcuts import render, redirect
# from django.urls import reverse

# from myngs.models import MyDashboardUserProfile


@login_required
def index(request):
    raise NotImplemented


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

    specialization = services \
        .store_specialization(student_uuid=uuid, specialization_uuid=specialization_uuid)

    return JsonResponse(specialization, safe=False)


def get_specializations(request, *args, **kwargs):
    faculty_param = request.GET.get('faculty')

    specializations = Specialization.objects.get(faculty=faculty_param)

    return JsonResponse(specializations, safe=False)


def get_student_suggestion(request, *args, **kwargs):
    name_param = request.GET.get('name')

    student_suggestions = StudentSuggestion.objects.get(name=name_param)

    response = []

    for student_suggestion in student_suggestions:
        (specialization,) = student_suggestion
        response.append(specialization)

    return JsonResponse(response, safe=False)
