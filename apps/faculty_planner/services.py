# from wand.image import Image as Img
import os
from PIL import Image
from pytesseract import image_to_string

from .models import Student, StudentSpecialization, Specialization


def store_specialization(student_uuid, specialization_uuid):
    student = Student.objects.get(uuid=student_uuid)

    specialization = Specialization.objects.get(uuid=specialization_uuid)

    student_specialization = StudentSpecialization \
        .objects.create(student=student, specialization=specialization)

    return student_specialization


# TODO: define service that will be used in the import part to save date

# with Img(filename='file_name.pdf', resolution=300) as img:
#     img.compression_quality = 99
#     img.save(filename='image_name.jpg')

# master info about students https://econ.ubbcluj.ro/documente2017/
# PDF example:
# https://econ.ubbcluj.ro/documente2015/01%20Lista%20candidati%20admisi%20pe%20programe%20MASTERAT%20ZI%20sept%202016.pdf
# documentation
# https://medium.com/@winston.smith.spb/python-ocr-for-pdf-or-compare-textract-pytesseract-and-pyocr-acb19122f38c
# good youtube video
# https://www.youtube.com/watch?v=-fIlUcp69xo
# https://stackoverflow.com/questions/35609773/oserror-errno-2-no-such-file-or-directory-using-pytesser
# https://stackoverflow.com/questions/20060096/installing-pil-with-pip
# early results based on test.png:
# 1 756 MICHIS 11V. BIANCAROSALIA 8,12 ADMIS
#
# z 9081 STANUS v [ARISAVVALENTINA 8,10 ADMIS
#
# 3 9027 ROATIS A. CARMENMARIA 7,73 ADMIS
#
# 4. 9118 BABALEAN M. MADALINA-EMANUELA 7,45 ADMIS
#
# 5, 9123 [LEA v. GEORGEBENIAMIN 7,38 ADMIS
#
# 6. 9125 POPU'I‘EA D CRISTIANVDANIEL 6,88 ADMIS
#
# 7. 9012 LUCAVDANILIU A STEFAN 6,83 ADMIS
#
# s. 9124 POPESCU v MlHAl 6,55 ADMIS

# FOR STRING SIMILARITY COMPARISION
# https://www.tools4noobs.com/online_tools/string_similarity/
# for poputea cristian daniel is 79.25%
# the lowest coeficency is 77.42% for Popescu Mihai

# TODO ask Horia about this
# Maybe in the interface suggest users to give complte name
# or the name that they have enrolled at the faculty

script_dir = os.path.dirname(__file__)
print(script_dir)
img_data = Image.open('/Users/cristian.poputea/projects/faculty-planner-django/apps/faculty_planner/test.png')

text = image_to_string(img_data)
print(text)
