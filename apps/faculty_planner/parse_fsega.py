from datetime import datetime

import lxml
from lxml.html import HtmlComment
from requests_html import HTMLSession

from .models import Faculty, Language, Specialization, Group, Room, \
    Professor, CourseDate, Course, DAY_IN_WEEK, Schedule, PARITY, SpecializationGroup, \
    ScheduleCourseDate, CourseDateGroup, COURSE_TYPE

FACULTY_ACRONYM = 'FSEGA'
PREPOSITIONS = [' si ', ' pe ', ' de ', ' a ', ' al ']
TEXT_STRING = ['\t', '\n', '\r']
FSEGA_URL_LOCATION = 'https://www.google.ro/maps/place/Faculty+of+Economics+and+Business+Administration/@46.773181,23.620944,15z/data=!4m2!3m1!1s0x0:0xcc357d4dedcf12a0?sa=X&ved=0ahUKEwiQjKWpuqbaAhUEmrQKHQNFBTIQ_BIInwEwCg'


# PAGE0 = https://econ.ubbcluj.ro/
# open the sidebar then search for "orar"
# then you will obtain the anchor tag that has the PAGE1 URL

def remove_substring_from_string(array_of_string, string, replace_character=""):
    for array_item in array_of_string:
        string = string.replace(array_item, replace_character)
    return string


def get_specialization_website_url():
    faculty = Faculty.objects.get(acronym=FACULTY_ACRONYM)
    session = HTMLSession()

    r = session.get(faculty.link)
    anchors = r.html.find("a")
    sem = 1

    result = faculty.link
    for anchor in anchors:
        if anchor.text.__contains__('Orar'):
            sem = anchor.text[-1]
            result += list(anchor.links)[0]

    create_specialization(faculty, result, sem)

    return result


# PAGE1 = https://econ.ubbcluj.ro/n2.php?id_c=135&id_m=7
# Create Specialization model
# Get faculty name
# Get sem
# Get all language
# Get degree type
# Get specialization name
# Get year
# Pillow for pdf to image

def create_specialization(faculty, link, sem):
    session = HTMLSession()

    r = session.get(link)
    # get element from path from chrome, right click on the element and copy path selector
    # remove tbody from searching, is not working
    td = r.html.find("body > table > tr:nth-child(1) > td > table > tr:nth-child(2) "
                     "> td > table > tr > td:nth-child(3) > table:nth-child(2) > tr > td")

    elem = lxml.html.fromstring(td[0].html)
    language = None

    for child_elem in elem.getchildren():

        if child_elem.tag == "p" and child_elem.attrib.get('align') == 'justify':
            language_ro = child_elem.getchildren()[5].text
            language = Language.objects.get_or_create(name=language_ro)[0]

        if child_elem.tag == "b":
            language_name = child_elem.text
            language = Language.objects.get_or_create(name=language_name)[0]

        if child_elem.tag == "ul":
            degree = ''

            for elem in child_elem.getchildren():
                if elem.tag == 'b' and elem.text == 'Orar Licenta':
                    degree = 'BACHELOR'
                if elem.tag == 'b' and elem.text == 'Orar Masterat':
                    degree = 'MASTER'

                if elem.tag == 'a':
                    link_specialization = faculty.link + elem.attrib.get("href")

                    name = elem.text[:-9]
                    name_for_acronym = remove_substring_from_string(PREPOSITIONS, name, " ")

                    acronym = "".join(e[0] for e in name_for_acronym.split())
                    year = int(elem.text[-1])

                    specialization = Specialization.objects \
                        .create(faculty=faculty, name=name, degree=degree, sem=int(sem), language=language,
                                link=link_specialization, acronym=acronym.upper(), year=year)

                    create_schedule(specialization)


def create_schedule(specialization):
    schedule = Schedule.objects.create(specialization=specialization)
    semi_groups_one = []
    semi_groups_two = []

    session = HTMLSession()

    r = session.get(specialization.link)
    # TODO investigate why doesn't add all course date on week
    # r = session.get('https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=MDAE&an=2')
    # r = session.get('https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=CIGF&an=3')
    # r = session.get("https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=AAG&an=2")
    # r = session.get('https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=EAM&an=2')

    # get element from path from chrome, right click on the element and copy path selector
    # remove tbody from searching, is not working
    # r.html.encoding = r.encoding
    try:
        table_path = r.html.find("#section-to-print > tr > td > table")

        table = lxml.html.fromstring(table_path[0].html)
        schedule_html = table.getchildren()[0]
        index_row = 0
        current_index_day = 0
        current_day_in_week = None

        for elem_row in schedule_html.getchildren():
            index_row += 1
            index_column = 0
            if index_row == 1:
                for elem_column in elem_row.getchildren():
                    if elem_column.tag == 'td':
                        index_column += 1
                        if index_column > 2:
                            span = elem_column.getchildren()[0]
                            group_name = span.text

                            group_name = remove_substring_from_string(TEXT_STRING, group_name)

                            group_one = Group.objects.create(name=group_name, sub_group=1)
                            group_two = Group.objects.create(name=group_name, sub_group=2)

                            SpecializationGroup.objects \
                                .create(specialization=specialization, group=group_one)
                            SpecializationGroup.objects \
                                .create(specialization=specialization, group=group_two)

                            semi_groups_one.append(group_one)
                            semi_groups_two.append(group_two)

            if index_row > 2:

                lower_group_index_limit = 0
                start_hour = ''
                end_hour = ''
                elem_row_children = elem_row.getchildren()

                if len(elem_row_children) and elem_row_children[0].attrib.get('rowspan', 0) != 0:
                    elem_row_children.pop(0)
                    current_day_in_week = DAY_IN_WEEK[current_index_day][0]
                if len(elem_row_children) == 1:
                    elem_row_children.pop(0)

                for elem_column in elem_row_children:
                    if elem_column.tag == "td":
                        index_column += 1
                    if elem_column.tag == "td" and index_column == 1:
                        # get hour from first td in the tr row
                        hour = elem_column.getchildren()[0].text.split('-')

                        lower_group_index_limit = 0
                        start_hour_text = hour[0]
                        start_hour_text = remove_substring_from_string(TEXT_STRING, start_hour_text)

                        start_hour = datetime.strptime(start_hour_text, "%H:%M")
                        end_hour = datetime.strptime(hour[1], "%H:%M")

                    if elem_column.tag == "td" and index_column > 1:
                        upper_group_index_limit = int(elem_column.attrib.get("colspan", 1))
                        elem_column = remove_comments(elem_column.getchildren())

                        if len(elem_column) > 0:
                            if elem_column[0].tag == "font":  # is a break (Pauza)
                                current_index_day += 1
                            else:
                                upper_group_index_limit += lower_group_index_limit

                                get_data_from_cell(
                                    elem_column=elem_column, specialization=specialization,
                                    start_hour=start_hour, end_hour=end_hour,
                                    lower_group_index_limit=lower_group_index_limit,
                                    upper_group_index_limit=upper_group_index_limit,
                                    semi_groups_one=semi_groups_one, semi_groups_two=semi_groups_two,
                                    current_day_in_week=current_day_in_week, schedule=schedule)

                                lower_group_index_limit = upper_group_index_limit

    except UnicodeDecodeError:
        # https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=EAM&an=2
        print("Error in request html for %s with the link: %s" % (specialization.name, specialization.link))


def remove_comments(html_elements):
    new_elems = []
    for html_element in html_elements:
        if not isinstance(html_element, HtmlComment):
            new_elems.append(html_element)
    return new_elems


def get_data_from_cell(elem_column, specialization, start_hour, end_hour,
                       current_day_in_week, schedule, lower_group_index_limit,
                       semi_groups_one, semi_groups_two, upper_group_index_limit):
    for div_elem in elem_column:
        span_elem = div_elem.getchildren()[0]

        span_child = span_elem.getchildren()

        if len(span_child) > 0:  # TODO: explore more
            if span_child[0].tag == "span":
                span_child = span_child[0].getchildren()
                if span_child[0].tag != "font":
                    span_child = span_child[0].getchildren()
            # take data from font tag
            room_name = span_child[0].text
            room = Room.objects.get_or_create(name=room_name, location=FSEGA_URL_LOCATION)[0]

            course_name = span_child[0].tail
            course_name = course_name[:-2]

            c_type = COURSE_TYPE[1][0]

            if course_name.isupper():
                c_type = COURSE_TYPE[0][0]  # is a seminar
            course = Course.objects.get_or_create(name=course_name, c_type=c_type)[0]

            professor_elem = span_child[1]
            professor_link = specialization.faculty.link + professor_elem.attrib.get("href", "")
            professor_name = professor_elem.text
            professor = Professor.objects.get_or_create(name=professor_name, link=professor_link)[0]

            week_type = ''
            week_type_opt = ''

            if len(span_child) > 2:
                week_type = span_child[2].text
                week_type_opt = span_child[2].tail

            parity_week = PARITY[2][0]
            is_sem_group_1 = True
            is_sem_group_2 = True

            if week_type == "SI":
                parity_week = PARITY[0][0]
            if week_type == "SP":
                parity_week = PARITY[1][0]

            if week_type_opt == "  - SI":
                parity_week = PARITY[0][0]
            if week_type_opt == "  - SP":
                parity_week = PARITY[1][0]

            if week_type_opt == "  - opt - Sg1":
                is_sem_group_2 = False
            if week_type_opt == "  - opt - Sg2":
                is_sem_group_1 = False

            if week_type == "Sg1":
                is_sem_group_2 = False
            if week_type == "Sg2":
                is_sem_group_1 = False

            course_date = CourseDate.objects \
                .create(course=course, room=room, professor=professor,
                        start_hour=start_hour, end_hour=end_hour, extra_info=week_type_opt,
                        day_in_week=current_day_in_week, parity_week=parity_week)

            # adding group for schedule
            for i in range(lower_group_index_limit, upper_group_index_limit):
                if i < len(semi_groups_one):
                    if is_sem_group_1:
                        CourseDateGroup.objects \
                            .create(group=semi_groups_one[i], course_date=course_date)
                    if is_sem_group_2:
                        CourseDateGroup.objects \
                            .create(group=semi_groups_two[i], course_date=course_date)
                else:
                    print("Error in %s for %s for course %s" %
                          (specialization.name, specialization.link, course_date.course.name))

            ScheduleCourseDate.objects \
                .create(schedule=schedule, course_date=course_date)


def add_professor_information():
    # read email
    return NotImplemented
