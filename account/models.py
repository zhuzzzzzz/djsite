from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    sex = models.CharField(max_length=1, null=True, blank=True, default='')
    birth_date = models.DateField(blank=True, null=True, default='')
    register_date = models.DateField(auto_now_add=True)
    introduce_text = models.CharField(max_length=50, blank=True, null=True, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile for user "{self.user}"'
