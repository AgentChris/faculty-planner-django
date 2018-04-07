from django.contrib import admin

from .models import Faculty, Specialization, Language, CourseDate


class FacultyAdmin(admin.ModelAdmin):
    model = Faculty


class LanguageAdmin(admin.ModelAdmin):
    model = Language


class SpecializationAdmin(admin.ModelAdmin):
    model = Specialization


class CourseDateAdmin(admin.ModelAdmin):
    model = CourseDate
    readonly_fields = ('start_hour', 'end_hour')


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(CourseDate, CourseDateAdmin)
