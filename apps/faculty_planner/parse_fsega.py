from requests_html import HTMLSession

from .models import Faculty

FACULTY_ACRONYM = 'FSEGA'

# PAGE0 = https://econ.ubbcluj.ro/
# open the sidebar then search for "orar"
# then you will obtain the anchor tag that has the PAGE1 URL


def get_specialization_website_url():
    faculty = Faculty.objects.get(acronym=FACULTY_ACRONYM)
    session = HTMLSession()

    r = session.get(faculty.link)
    anchors = r.html.find("a")
    result = ""
    for anchor in anchors:
        if anchor.text.__contains__('Orar'):
            result = anchor.links

    return result


# PAGE1 = https://econ.ubbcluj.ro/n2.php?id_c=135&id_m=7
# Create Specialization model
# Get faculty name
# Get sem
# Get all language
# Get degree type
# Get specialization name
# Get year

# For each specialization first do this and then go for the next specialization
# https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=CIG&an=1
# https://econ.ubbcluj.ro/orar/orar-sem-2.php?acronim=CIG&an=2
# etc
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
