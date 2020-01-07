from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    NORMAL, MANAGER = range(2)
    ROLES = (
        (NORMAL, 'Normal'),
        (MANAGER, 'Manger'),
    )
    role = models.PositiveIntegerField(choices=ROLES, default=NORMAL)
    def __str__(self):
        return self.email
