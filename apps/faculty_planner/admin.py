from django.contrib import admin

from .models import Faculty, Specialization, Language, \
    CourseDate, Schedule, Professor, Course, Group


class GroupAdmin(admin.ModelAdmin):
    model = Group


class CourseAdmin(admin.ModelAdmin):
    model = Course


class ProfessorAdmin(admin.ModelAdmin):
    model = Professor


class FacultyAdmin(admin.ModelAdmin):
    model = Faculty


class LanguageAdmin(admin.ModelAdmin):
    model = Language


class CourseDateInline(admin.TabularInline):
    model = CourseDate


class CourseDatesGroupInline(admin.TabularInline):
    model = CourseDate.groups.through
    extra = 0


class ScheduleCourseDatesInline(admin.TabularInline):
    model = Schedule.course_dates.through
    extra = 0


class ScheduleAdminForm(admin.ModelAdmin):
    inlines = [ScheduleCourseDatesInline, ]


class SpecializationAdmin(admin.ModelAdmin):
    model = Specialization


class CourseDateAdminForm(admin.ModelAdmin):
    inlines = [CourseDatesGroupInline, ]
    model = CourseDate
    readonly_fields = ('updated',)


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Schedule, ScheduleAdminForm)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(CourseDate, CourseDateAdminForm)
