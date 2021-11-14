from django.db import models
from django.utils.translation import ugettext_lazy as _


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

    subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

class Exercise(models.Model):

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    image_description = models.ImageField(upload_to='descriptions')
    text_description = models.TextField()
    image_answer = models.ImageField(upload_to='answers')
    text_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Exercise {self.module}"
