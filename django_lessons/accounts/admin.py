from django.contrib import admin
from .forms import StudentAccountRegisterForm, TutorAccountForm
from .models import (Messages, StudentProfile, StudentUser, TutorProfile,
                     TutorUser)


@admin.register(TutorUser)
class TutorUsers(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'email', 'is_staff', 'is_subscriber')
    list_filter = ('is_staff',)
    fields = ('username', 'first_name', 'last_name', 'email',
              'is_staff', 'is_student', 'is_subscriber')
    form = TutorAccountForm


@admin.register(StudentUser)
class StudentUsers(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'is_student', 'is_subscriber')
    list_filter = ('is_student',)
    fields = ('username', 'first_name', 'last_name',
              'email', 'is_student', 'is_subscriber')
    form = StudentAccountRegisterForm


@admin.register(StudentProfile)
class StudentProfiles(admin.ModelAdmin):
    list_display = ('user', 'image', 'location', 'phone_number')


@admin.register(TutorProfile)
class TutorProfiles(admin.ModelAdmin):
    list_display = ('user', 'image', 'location', 'phone_number')


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('student_user', 'title')
