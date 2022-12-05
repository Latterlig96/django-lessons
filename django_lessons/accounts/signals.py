from app.models import Activities
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .models import StudentProfile, StudentUser, TutorProfile, TutorUser


@receiver(post_save, sender=StudentUser)
def create_student_profile_signal(
    sender: StudentUser, instance: StudentUser, created: bool, **kwargs
) -> None:
    if created:
        StudentProfile.objects.create(user=instance)
        activities = Activities.objects.create(student=instance)
        activities.description = _(
            "Created profile for %(name)s %(surname)s"
            % {"name": instance.first_name, "surname": instance.last_name}
        )
        activities.save()


@receiver(post_save, sender=TutorUser)
def create_tutor_profile_signal(
    sender: TutorUser, instance: TutorUser, created: bool, **kwargs
) -> None:
    if created:
        TutorProfile.objects.create(user=instance)
