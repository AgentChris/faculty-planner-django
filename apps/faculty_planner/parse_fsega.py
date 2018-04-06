import lxml.html
from requests_html import HTMLSession

from .models import Faculty, Language, Specialization, Group

FACULTY_ACRONYM = 'FSEGA'
PREPOSITIONS = ['si', 'pe', 'de', 'a', 'al']
TEXT_STRING = ['\t', '\n', '\r']


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
    session = HTMLSession()

    r = session.get(specialization.link)
    # get element from path from chrome, right click on the element and copy path selector
    # remove tbody from searching, is not working
    table_path = r.html.find("#section-to-print > tr > td > table")

    table = lxml.html.fromstring(table_path[0].html)
    schedule_html = table.getchildren()[0]
    index_row = 0

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

                        group = Group.objects.create(name=group_name)
                        specialization.groups.add(group)

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
