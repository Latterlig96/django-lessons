from django.forms import ModelForm
from .models import Subject, Module, Exercise


class SubjectForm(ModelForm):

    class Meta:
        model = Subject
        fields = '__all__'

class ModuleForm(ModelForm):

    class Meta:
        model = Module
        fields = '__all__'

class ExerciseForm(ModelForm):

    class Meta:
        model = Exercise
        fields = '__all__'
