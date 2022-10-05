from django.contrib import admin
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import StudentAccountRegisterForm, TutorAccountForm
from .models import Messages, StudentProfile, StudentUser, TutorProfile, TutorUser


@admin.register(TutorUser)
class TutorUsers(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_subscriber",
    )
    list_filter = ("is_staff",)
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_student",
        "is_subscriber",
    )
    form = TutorAccountForm


@admin.register(StudentUser)
class StudentUsers(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "is_student", "is_subscriber")
    list_filter = ("is_student",)
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_student",
        "is_subscriber",
    )
    form = StudentAccountRegisterForm
    actions = ["make_subscriber"]

    @admin.action(description="Make student a subscriber and email them about this")
    def make_subscriber(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(is_subscriber=True)
        html_message = render_to_string("order/email_notify.html")
        plain_message = strip_tags(html_message)
        send_mail(
            "Purchase Approved",
            plain_message,
            request.user.email,
            [student.email for student in queryset.iterator()],
            fail_silently=False,
        )


@admin.register(StudentProfile)
class StudentProfiles(admin.ModelAdmin):
    list_display = ("user", "image", "location", "phone_number")


@admin.register(TutorProfile)
class TutorProfiles(admin.ModelAdmin):
    list_display = ("user", "image", "location", "phone_number")


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("student_user", "title")
