from django.db import models


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="ingredients"
    )
    name = models.CharField(max_length=64)
    amount = models.CharField(max_length=20)
    unit = models.CharField(max_length=16, null=True, blank=True)
    note = models.TextField(blank=True)


class Recipe(models.Model):
    title = models.CharField(max_length=128)
    directions = models.TextField()
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, related_name="recipes", null=True, blank=True
    )
    category = models.CharField(null=True, blank=True, max_length=32)

    prep_time = models.IntegerField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)

    likes = models.IntegerField(default=0, blank=True, editable=False)
    dislikes = models.IntegerField(default=0, blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
