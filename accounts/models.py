from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        LEARNER = "LEARNER", "Learner"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.LEARNER,
    )

    def __str__(self):
        return self.username


class LearnerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="learner_profile",
    )

    preferred_language = models.ForeignKey(
        "languages.Language",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learners",
    )

    bio = models.TextField(blank=True)

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"