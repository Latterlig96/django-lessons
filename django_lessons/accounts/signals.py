from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, StudentUser, TutorProfile, TutorUser
from app.models import Activities

@receiver(post_save, sender=StudentUser)
def create_student_profile_signal(sender: StudentUser,
                                  instance: StudentUser,
                                  created: bool, **kwargs) -> None:
    if created:
        StudentProfile.objects.create(user=instance)
        activities = Activities.objects.create(student=sender)
        activities.description = f"Created profile for {sender.first_name} {sender.last_name}"
        activities.save()

@receiver(post_save, sender=TutorUser)
def create_tutor_profile_signal(sender: TutorUser,
                                instance: TutorUser,
                                created: bool, **kwargs) -> None:
    if created:
        TutorProfile.objects.create(user=instance)
