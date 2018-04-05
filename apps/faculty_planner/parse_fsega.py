from requests_html import HTMLSession

from .models import Faculty, Language, Specialization

FACULTY_ACRONYM = 'FSEGA'


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
    td = r.html.find("td")

    for child_elem in td:
        language = None
        lists_ul = []

        if child_elem.type == "ul":
            lists_ul = child_elem

        if child_elem.type == "p" and child_elem.proptype == "justify":
            language_ro = child_elem.child.text
            language = Language.objects.get_or_create(name=language_ro)

        if child_elem.type == "b":
            language_name = child_elem.text
            language = Language.objects.get_or_create(name=language_name)

        degree = ''
        for childs_ul in lists_ul:
            for elem in childs_ul:
                if elem.type == 'b' and elem.text == 'Orar Licenta':
                    degree = 'BACHELOR'
                if elem.type == 'b' and elem.text == 'Orar Masterat':
                    degree = 'MASTER'

                if elem.type == 'a':
                    link = elem.link
                    elem_text = elem.text.split('-')
                    name = elem_text[0]
                    acronym = filter(str.isupper, name)
                    year = int(elem_text[1][-1])

                    Specialization.objects \
                        .create(faculty=faculty, language=language, name=name, degree=degree,
                                link=link, acronym=acronym, year=year, sem=sem)


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
