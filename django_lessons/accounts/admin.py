from django.contrib import admin
from .models import StudentUser, TutorUser
from .forms import StudentAccountForm, TutorAccountForm


@admin.register(TutorUser)
class TutorUsers(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    fields = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    form = TutorAccountForm

@admin.register(StudentUser)
class StudentUsers(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    fields = ('username', 'first_name', 'last_name', 'email')
    form = StudentAccountForm
