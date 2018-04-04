from django.contrib import admin

from .models import Faculty


class FacultyAdmin(admin.ModelAdmin):
    model = Faculty


admin.site.register(Faculty, FacultyAdmin)
