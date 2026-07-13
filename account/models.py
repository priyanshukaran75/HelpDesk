from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    department = models.CharField(
        max_length=100,
        default="System Department"
    )
    phone = models.CharField(
        max_length=15,
        blank=True
    )
    designation = models.CharField(
        max_length=100,
        blank=True
    )
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    def __str__(self):
        return self.user.username
# Create your models here.
