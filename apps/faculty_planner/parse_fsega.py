from datetime import datetime

import lxml
from lxml.html import HtmlComment
from requests_html import HTMLSession

from .models import Faculty, Language, Specialization, Group, Room, \
    Professor, CourseDate, Course, DAY_IN_WEEK, Schedule, PARITY, SpecializationGroup, \
    ScheduleCourseDate

FACULTY_ACRONYM = 'FSEGA'
PREPOSITIONS = ['si', 'pe', 'de', 'a', 'al']
TEXT_STRING = ['\t', '\n', '\r']
FSEGA_URL_LOCATION = 'https://www.google.ro/maps/place/Faculty+of+Economics+and+Business+Administration/@46.773181,23.620944,15z/data=!4m2!3m1!1s0x0:0xcc357d4dedcf12a0?sa=X&ved=0ahUKEwiQjKWpuqbaAhUEmrQKHQNFBTIQ_BIInwEwCg'


# PAGE0 = https://econ.ubbcluj.ro/
# open the sidebar then search for "orar"
# then you will obtain the anchor tag that has the PAGE1 URL


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
                    for prep in PREPOSITIONS:
                        name = name.replace(' ' + prep, '')
                    acronym = "".join(e[0] for e in name.split())
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
    # r = session.get('https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=EAM&an=2')

    # get element from path from chrome, right click on the element and copy path selector
    # remove tbody from searching, is not working
    r.html.encoding = r.encoding
    try:
        table_path = r.html.find("#section-to-print > tr > td > table")

        table = lxml.html.fromstring(table_path[0].html)
        schedule_html = table.getchildren()[0]
        index_row = 1
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
                            for CHR in TEXT_STRING:
                                group_name = group_name.replace(CHR, '')

                            group_one = Group.objects.create(name=group_name, sub_group=1)
                            group_two = Group.objects.create(name=group_name, sub_group=2)

                            SpecializationGroup.objects \
                                .create(specialization=specialization, group=group_one)
                            SpecializationGroup.objects \
                                .create(specialization=specialization, group=group_one)

                            semi_groups_one.append(group_one)
                            semi_groups_two.append(group_two)

            if index_row > 2:

                group_lower_limit = 0
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
                        hour = elem_column.getchildren()[0].text.split('-')
                        start_hour_text = hour[0]
                        for CHR in TEXT_STRING:
                            start_hour_text = start_hour_text.replace(CHR, '')
                        start_hour = datetime.strptime(start_hour_text, "%H:%M")
                        end_hour = datetime.strptime(hour[1], "%H:%M")
                    if elem_column.tag == "td" and index_column > 1:
                        # group_upper_limit = elem_column.attrib.get("colspan", 1)
                        elem_column = remove_comments(elem_column.getchildren())

                        if len(elem_column) > 0:
                            if elem_column[0].tag == "font":  # is a break (Pauza)
                                current_index_day += 1
                            else:
                                course_date = get_data_from_cell(
                                    elem_column=elem_column, specialization=specialization,
                                    start_hour=start_hour, end_hour=end_hour,
                                    current_day_in_week=current_day_in_week)
                                if course_date:
                                    ScheduleCourseDate.objects \
                                        .create(schedule=schedule, course_date=course_date)
    except UnicodeDecodeError:
        # https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=EAM&an=2
        print("Error in request html for %s with the link: %s" % (specialization.name, specialization.link))
        # for i in range(group_lower_limit, group_upper_limit):
        #     semi_group_one = semi_groups_one[i]
        #     semi_group_two = semi_groups_two[i]
        #
        #     if is_sem_group_1:
        #         CourseDateGroup.objects \
        #             .create(course_date=course_date, group=semi_group_one)
        #     if is_sem_group_2:
        #         CourseDateGroup.objects \
        #             .create(course_date=course_date, group=semi_group_two)
        #
        # group_lower_limit = group_upper_limit


def remove_comments(html_elements):
    new_elems = []
    for html_element in html_elements:
        if not isinstance(html_element, HtmlComment):
            new_elems.append(html_element)
    return new_elems


def get_data_from_cell(elem_column, specialization, start_hour, end_hour, current_day_in_week):
    course_date = None

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
            course = Course.objects.get_or_create(name=course_name)[0]

            professor_elem = span_child[1]
            professor_link = specialization.faculty.link + professor_elem.attrib.get("href", "")
            professor_name = professor_elem.text
            professor = Professor.objects.get_or_create(name=professor_name, link=professor_link)[0]

            week_type = ''
            if len(span_child) > 2:
                week_type = span_child[2].text

            parity_week = PARITY[2][0]
            is_sem_group_1 = True
            is_sem_group_2 = True

            if week_type == "SI":
                parity_week = PARITY[0][0]
            if week_type == "SP":
                parity_week = PARITY[1][0]

            # TODO add to semigroup
            # TODO add groups
            # TODO add course optional
            # TODO add course type uppercase - Course, lowercase - Semniar
            # TODO add course reading from semigroup

            if week_type == "Sg1":
                is_sem_group_2 = False
            if week_type == "Sg2":
                is_sem_group_1 = False

            course_date = CourseDate.objects \
                .create(course=course, room=room, professor=professor,
                        start_hour=start_hour, end_hour=end_hour,
                        day_in_week=current_day_in_week, parity_week=parity_week)

        return course_date


# https://econ.ubbcluj.ro/cv.php?id=350
def add_professor_information():
    # read email
    return NotImplemented

# Create SpecializationGroup
# open every link from PAGE1 SEE ABOVE

# Create a Schedule for each group
# ? not sure about anymore maybe in phase one we won't need it
# maybe we can create a schdule for each student, the initial one will be the one crate
# by the faculty and then the student can add more course dates
# but in phase we won't do that


# Create all Groups for specializations
# Create Course Date

# first crate schdule then add it to group by creating SchduleGroup Object
