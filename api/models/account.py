from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=128)

    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    onboarded = models.BooleanField(default=False)

    def __str__(self):
        return self.email
