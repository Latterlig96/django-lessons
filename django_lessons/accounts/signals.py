from .models import StudentUser, TutorUser, StudentProfile, TutorProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=StudentUser)
def create_student_profile_signal(sender: StudentUser, 
                               instance: StudentUser, 
                               created: bool, **kwargs) -> None:
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=TutorUser)
def create_tutor_profile_signal(sender: TutorUser, 
                               instance: TutorUser, 
                               created: bool, **kwargs) -> None:
    if created:
        TutorProfile.objects.create(user=instance)
