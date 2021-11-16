from django.contrib import admin
from .models import Subject, Module, Exercise
from .forms import SubjectForm, ModuleForm, ExerciseForm


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    fields = ('subject',)
    form = SubjectForm

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'title', 'description', 'created_at')
    fields = ('subject', 'title', 'description')
    list_filter = ('created_at',)
    form = ModuleForm

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('module', 'image_description', 'text_description',
                    'image_answer', 'text_answer', 'created_at')
    fields = ('module', 'image_description', 'text_description',
              'image_answer', 'text_answer')
    list_filter = ('created_at',)
    form = ExerciseForm
