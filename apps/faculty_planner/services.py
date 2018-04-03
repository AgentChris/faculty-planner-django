from .models import Student, StudentSpecialization, Specialization


def store_specialization(student_uuid, specialization_uuid):
    student = Student.objects.get(uuid=student_uuid)

    specialization = Specialization.objects.get(uuid=specialization_uuid)

    student_specialization = StudentSpecialization \
        .objects.create(student=student, specialization=specialization)

    return student_specialization

# TODO: define service that will be used in the import part to save date


