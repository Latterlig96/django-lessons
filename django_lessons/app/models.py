from accounts.models import StudentUser
from django.db import models
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.db.models.functions import ExtractDay, ExtractMonth
from django.db.models import Count


class SupportedSubjects(models.TextChoices):

    MATH = "Math", _("Math")
    CHEMISTRY = "Chemistry", _("Chemistry")
    PHYSICS = "Physics", _("Physics")


class Subject(models.Model):

    subject = models.CharField(max_length=50, choices=SupportedSubjects.choices)

    def __str__(self) -> str:
        return self.subject

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_subject_constraint",
                check=models.Q(subject__in=SupportedSubjects.values),
            )
        ]


class Module(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return self.title


class Exercise(models.Model):

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.TextField()
    image_description = models.ImageField(
        upload_to="descriptions", blank=True, null=True
    )
    text_description = models.TextField()
    exercise_image_answer = models.ImageField(
        upload_to="answers", blank=True, null=True
    )
    exercise_text_answer = models.TextField()
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"Exercise {self.module}"

    def get_absolute_url(self) -> HttpResponse:
        return reverse_lazy(
            "app:exercise", kwargs={"module_id": self.module.pk, "pk": self.pk}
        )


class Answer(models.Model):

    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    answer_image = models.ImageField(upload_to="answers", blank=True)
    answer_text = models.TextField()

    def __str__(self) -> str:
        return f"{self.student} answer for {self.exercise}"


class Favorites(models.Model):

    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Favorite exercises for student {self.student.first_name} {self.student.last_name}"


class Activities(models.Model):

    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return (
            f"Activities of student {self.student.first_name} {self.student.last_name}"
        )
        
    @classmethod
    def get_monthly_activities(cls, student: StudentUser) -> QuerySet:
        return cls.objects\
            .filter(student=student)\
            .annotate(month=ExtractMonth("created_at"))\
            .values("month")\
            .annotate(count=Count("month"))\
            .order_by("month")\
            .values("month", "count")\
            .get() # type: ignore

    @classmethod
    def get_daily_activities(cls, student: StudentUser) -> QuerySet:
        return cls.objects\
            .filter(student=student)\
            .annotate(day=ExtractDay("created_at"))\
            .values("day")\
            .annotate(count=Count("day"))\
            .order_by("day")\
            .values("day", "count")\
            .get() # type: ignore
