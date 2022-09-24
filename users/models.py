from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from utils.models import BaseModel
from utils import generate_file_name


class User(AbstractUser):
    """
    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Profile(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_profile",
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __unicode__(self):
        return f"{self.user}"

    def __str__(self) -> str:
        return f"{self.user}"
