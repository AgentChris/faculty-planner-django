from django.contrib import admin

from .models import Faculty, Specialization


class FacultyAdmin(admin.ModelAdmin):
    model = Faculty


class SpecializationAdmin(admin.ModelAdmin):
    model = Specialization


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Specialization, SpecializationAdmin)
