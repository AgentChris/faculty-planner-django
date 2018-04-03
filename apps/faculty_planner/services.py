from .models import Student, Group, StudentSpecialization, SpecializationGroup, Specialization


def store_specialization(student_uuid, specialization_uuid):
    student = Student.objects.get(uuid=student_uuid)

    specialization = Specialization.objects.get(uuid=specialization_uuid)

    student_specialization = StudentSpecialization \
        .objects.create(student=student, specialization=specialization)

    return student_specialization



