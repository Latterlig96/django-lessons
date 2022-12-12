from django import forms
from django.forms import ModelForm
from django.forms.widgets import FileInput
from django.utils.translation import gettext_lazy as _

from .models import Answer, Exercise, Favorites, Module, Subject


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = "__all__"


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"


class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].widget = forms.HiddenInput()
        self.fields["exercise"].widget = forms.HiddenInput()

    class Meta:
        model = Answer
        fields = "__all__"
        widgets = {
            "answer_image": FileInput(
                attrs={"id": "answer_image", "placeholder": _("Image Answer")}
            )
        }


class FavoritesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget = forms.HiddenInput()

    class Meta:
        model = Favorites
        fields = "__all__"


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    message = forms.CharField(max_length=500, required=True)
