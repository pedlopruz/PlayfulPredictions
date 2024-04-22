from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    puntos = models.IntegerField(default=0)
    last_login = models.DateTimeField(auto_now=True)