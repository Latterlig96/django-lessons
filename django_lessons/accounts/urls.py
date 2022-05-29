from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.StudentRegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("students/", views.StudentListView.as_view(), name="students"),
    path("students/<pk>/profile", views.StudentProfileView.as_view(), name="profile"),
    path("tutors/<pk>/profile", views.TutorProfileView.as_view(), name="tutor_profile"),
    path("profile/<pk>/messages", views.MessageListView.as_view(), name="messages"),
    path(
        "profile/<pk>/messages/<int:message_id>",
        views.MessageDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "profile/<pk>/message/<int:student_id>",
        views.MessageFormView.as_view(),
        name="message_form",
    ),
    path(
        "profile/<pk>/settings/",
        views.StudentUserSettingsView.as_view(),
        name="settings",
    ),
    path(
        "tutors/<pk>/settings/",
        views.TutorUserSettingsView.as_view(),
        name="tutor_settings",
    ),
    path("password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password/change/done",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
