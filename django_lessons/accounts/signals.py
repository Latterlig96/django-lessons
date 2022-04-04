from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Activities

from .models import StudentProfile, StudentUser, TutorProfile, TutorUser


@receiver(post_save, sender=StudentUser)
def create_student_profile_signal(sender: StudentUser,
                                  instance: StudentUser,
                                  created: bool, **kwargs) -> None:
    if created:
        StudentProfile.objects.create(user=instance)
        activities = Activities.objects.create(student=instance)
        activities.description = f"Created profile for {instance.first_name} {instance.last_name}"
        activities.save()

@receiver(post_save, sender=TutorUser)
def create_tutor_profile_signal(sender: TutorUser,
                                instance: TutorUser,
                                created: bool, **kwargs) -> None:
    if created:
        TutorProfile.objects.create(user=instance)

@receiver(user_logged_in, sender=StudentUser)
def student_logged_in_signal(sender: StudentUser,
                             instance: StudentUser,
                             request,
                             **kwargs) -> None:
    activities = Activities.objects.create(student=instance)
    activities.description = f"Logged in"
    activities.save()
