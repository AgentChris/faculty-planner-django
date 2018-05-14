from django.contrib import admin

from .models import Faculty, Specialization, Language, \
    CourseDate, Schedule, Professor, Course, Group, Room, \
    YearStructure


class GroupAdmin(admin.ModelAdmin):
    model = Group


class RoomAdmin(admin.ModelAdmin):
    model = Room


class CourseAdmin(admin.ModelAdmin):
    model = Course


class ProfessorAdmin(admin.ModelAdmin):
    model = Professor


class FacultyAdmin(admin.ModelAdmin):
    model = Faculty


class LanguageAdmin(admin.ModelAdmin):
    model = Language


class DayTypeInline(admin.TabularInline):
    model = YearStructure.days.through
    extra = 0


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


class SpecializationGroupInline(admin.TabularInline):
    model = Specialization.groups.through
    extra = 0


class SpecializationAdmin(admin.ModelAdmin):
    inlines = [SpecializationGroupInline, ]
    model = Specialization


class CourseDateAdminForm(admin.ModelAdmin):
    inlines = [CourseDatesGroupInline, ]
    model = CourseDate
    readonly_fields = ('updated',)


class YearStructureAdminForm(admin.ModelAdmin):
    inlines = [DayTypeInline, ]
    model = YearStructure


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Schedule, ScheduleAdminForm)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(CourseDate, CourseDateAdminForm)
admin.site.register(YearStructure, YearStructureAdminForm)
