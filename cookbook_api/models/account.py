from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=128, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=128)

    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    onboarded = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# for now, it is not editable
class Comment(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="comments")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(editable=False)

    likes = models.IntegerField(default=0, blank=True, editable=False)
    dislikes = models.IntegerField(default=0, blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
