import json
from datetime import datetime

import pandas as pd
from django.db.utils import IntegrityError
from django.http import JsonResponse
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.views import ProtectedResourceView
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404

from .models import StudentSuggestion, Specialization, Schedule, CourseDate, YearStructure, Faculty, Student, \
    StudentSpecialization
from .parse_fsega import get_specialization_website_url, add_professor_information
from .serializers import SpecializationSerializer, CourseDateSerializer, DayTypeSerializer, StudentSerializer
from .services import store_specialization
from .utils import SmallResultsSetPagination


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


def store_student_specialization(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # TODO: get uuid from jwt token, and then remove the hardcoded uuid
    uuid = "12312"

    specialization_uuid = body.get('specialization_uuid')

    specialization = store_specialization(student_uuid=uuid, specialization_uuid=specialization_uuid)

    return JsonResponse(specialization, safe=False)


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


class StudentView(mixins.RetrieveModelMixin, mixins.ListModelMixin, ProtectedResourceView, viewsets.GenericViewSet):
    queryset = Student.objects.all()
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = Student

    def list(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.resource_owner)

        student_serializer = StudentSerializer(student)

        return JsonResponse(student_serializer.data, safe=False)

    def create(self, request, *args, **kwargs):
        body = request.data

        name = body.get('name')
        email = body.get('email')

        student, created = Student.objects.get_or_create(name=name, email=email, user=request.resource_owner)

        student_serializer = StudentSerializer(student, many=False)

        return JsonResponse(student_serializer.data, safe=False)


class SpecializationView(mixins.ListModelMixin, ProtectedResourceView, viewsets.GenericViewSet):
    queryset = Specialization.objects.all()
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = SpecializationSerializer
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `faculty acronym` query parameter in the URL.
        """
        queryset = Specialization.objects.all()
        faculty_param = self.request.query_params.get('faculty', None)
        if faculty_param is not None:
            queryset = queryset.filter(faculty__acronym=faculty_param)
        return queryset

    @detail_route(methods=['post'])
    def assign_student(self, request, pk=None):
        specialization = Specialization.objects.get(uuid=pk)
        student = Student.objects.get(user=request.resource_owner)

        try:
            StudentSpecialization.objects.create(specialization=specialization, student=student)
        except IntegrityError as e:
            return JsonResponse({"message": "You already added this specialization"}, safe=False)

        specialization_serializer = SpecializationSerializer(specialization, many=False)

        return JsonResponse(specialization_serializer.data, safe=False)


class CourseDatesView(mixins.RetrieveModelMixin, mixins.ListModelMixin, ProtectedResourceView, viewsets.GenericViewSet):
    queryset = CourseDate.objects.all()
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CourseDateSerializer

    def list(self, request, *args, **kwargs):
        group_uuid_param = request.GET.get('group')
        start_date_param = request.GET.get('start_date')
        end_date_param = request.GET.get('end_date')
        only_dates_param = request.GET.get('only_dates')

        start_date = None
        end_date = None

        only_dates = False
        if only_dates_param == 'true':
            only_dates = True

        if start_date_param:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d')
        if end_date_param:
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d')

        course_dates = CourseDate.objects.filter(groups__uuid__contains=group_uuid_param)

        specialization = Specialization.objects.get(groups__uuid__contains=group_uuid_param)

        faculty = specialization.faculty
        year = specialization.year
        sem = specialization.sem
        degree = specialization.degree

        final = False
        # TODO this rule may vary bettween faculties
        # here i determine the final years
        if ((degree == 'DOCTORAL' or degree == 'MASTER') and
            year == 2) or (final == 'BACHELOR' and year == 3):
            final = True

        year_structures = YearStructure.objects \
            .filter(faculty=faculty, year=2018, sem=sem, final_years=final)

        response = []
        if year_structures:
            for period in year_structures.first().days.all():
                if period.type == 'F':  # if is a period of days which is a FACULTY_DAY then this is the schedule

                    date_range = pd.date_range(period.start_date, period.end_date)

                    week_index = 0
                    is_week_odd = True  # determine if week is odd or even
                    for single_date in date_range:

                        week_index += 1
                        if week_index == 6:
                            week_index = 0
                            is_week_odd = not is_week_odd

                        if (start_date and single_date < start_date) or (end_date and single_date > end_date):
                            continue

                        if len(course_dates) > 0:
                            day_index = single_date.date().weekday()
                            response_item = {"date": single_date.strftime("%Y-%m-%d")}

                                response_item["course_dates"] = []
                                for course_date in course_dates:
                                    day_in_week = course_date.day_in_week
                                    parity_week = course_date.parity_week

                                    # check to see if the current day is valid for the current course_date
                                    if parity_week == 'W' or (is_week_odd and parity_week == 'O') \
                                        or (not is_week_odd and parity_week == 'E'):

                                        if day_in_week == 'MON' and day_index == 0 or \
                                            day_in_week == 'TUES' and day_index == 1 or \
                                            day_in_week == 'WED' and day_index == 2 or \
                                            day_in_week == 'THURS' and day_index == 3 or \
                                            day_in_week == 'FRI' and day_index == 4 or \
                                            day_in_week == 'SAT' and day_index == 5 or \
                                            day_in_week == 'SUN' and day_index == 6:
                                            course_date_data = CourseDateSerializer(course_date, many=False)
                                            response_item['course_dates'].append(course_date_data.data)

                            has_course_dates = len(response_item['course_dates']) > 0
                            if only_dates:
                                del response_item['course_dates']

                            if has_course_dates:
                            response.append(response_item)

        return JsonResponse(response, safe=False)

    def retrieve(self, request, pk=None):
        course_date = get_object_or_404(CourseDate, uuid=pk)
        course_date_serializer = CourseDateSerializer(course_date)

        return JsonResponse(course_date_serializer.data, safe=False)
