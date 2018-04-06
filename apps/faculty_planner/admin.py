from django.contrib import admin

from .models import Faculty, Specialization, Language


class FacultyAdmin(admin.ModelAdmin):
    model = Faculty


class LanguageAdmin(admin.ModelAdmin):
    model = Language


class SpecializationAdmin(admin.ModelAdmin):
    model = Specialization


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Specialization, SpecializationAdmin)
