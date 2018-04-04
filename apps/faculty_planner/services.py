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
script_dir = os.path.dirname(__file__)
print(script_dir)
img_data = Image.open('/Users/cristian.poputea/projects/faculty-planner-django/apps/faculty_planner/test.png')

text = image_to_string(img_data)
print(text)
