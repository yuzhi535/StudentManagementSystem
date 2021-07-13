from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from StudentManagementApp.models import CustomUser, Student, Course, Staff, Study, Admin, StuClass


class UserModel(UserAdmin):
    model = CustomUser


admin.site.register(CustomUser, UserModel)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Course)
admin.site.register(Study)
admin.site.register(Admin)
admin.site.register(StuClass)
# admin.site.register(Course, UserModel)
