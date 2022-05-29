from django.contrib import admin

from .forms import ExerciseForm, ModuleForm, SubjectForm
from .models import Exercise, Module, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("subject",)
    fields = ("subject",)
    form = SubjectForm


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("subject", "title", "description", "created_at")
    fields = ("subject", "title", "description")
    list_filter = ("created_at",)
    form = ModuleForm


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "module",
        "title",
        "image_description",
        "text_description",
        "image_answer",
        "text_answer",
        "is_premium",
        "created_at",
    )
    fields = (
        "module",
        "title",
        "image_description",
        "text_description",
        "image_answer",
        "is_premium",
        "text_answer",
    )
    list_filter = ("created_at",)
    form = ExerciseForm
