from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from accounts.models import StudentUser
from typing import TypeVar

_HttpResponse = TypeVar('_HttpResponse')

class Subject(models.Model):

    SUBJECT_CHOICES = [
        ('Math', _('Math')),
        ('Chemistry', _('Chemistry')),
        ('Physics', _('Physics'))
    ]

    subject = models.CharField(verbose_name='subjects', max_length=50, choices=SUBJECT_CHOICES)

    def __str__(self):
        return self.subject

class Module(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title

class Exercise(models.Model):

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.TextField()
    image_description = models.ImageField(upload_to='descriptions', blank=True)
    text_description = models.TextField()
    image_answer = models.ImageField(upload_to='answers', blank=True)
    text_answer = models.TextField()
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"Exercise {self.module}"
    
    def get_absolute_url(self) -> _HttpResponse:
        return reverse_lazy('app:exercise', kwargs={'module_id': self.module.pk, 'pk': self.pk})

class Answer(models.Model):

    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    image_answer = models.ImageField(upload_to='answers', blank=True)
    text_answer = models.TextField()

    def __str__(self): 
        return f"{self.student} answer for {self.exercise}"

class Favorites(models.Model):

    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite exercises for student {self.student.first_name} {self.student.last_name}"
