from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    num = models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    puntos = models.IntegerField(default=0)
    last_login = models.DateTimeField(auto_now=True)
    terminos = models.BooleanField(default=False)