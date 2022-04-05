from django.db import models


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="ingredients"
    )
    name = models.CharField(max_length=64)
    amount = models.CharField(max_length=20)
    unit = models.CharField(max_length=16, null=True, blank=True)
    note = models.TextField(blank=True)


class Direction(models.Model):
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="directions"
    )
    order = models.IntegerField(null=True, blank=True)
    direction = models.TextField()


class Recipe(models.Model):

    class Category(models.TextChoices):
        MAIN_COURSE = 'main course'
        SIDE_DISH = 'side dish'
        DESSERT = 'desert'
        APPETIZER = 'appetizer'
        SALAD = 'salad'
        BREAKFAST = 'breakfast'
        SOUP = 'soup'
        SNACK = 'snack'
        BEVERAGE = 'beverage'

    class Difficulty(models.TextChoices):
        EASY = 'easy'
        MODERATE = 'moderate'
        HARD = 'hard'

    title = models.CharField(max_length=128)
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, related_name="recipes", null=True, blank=True
    )
    image = models.ImageField(upload_to='recipes/images')
    category = models.CharField(max_length=20, choices=Category.choices, null=True)
    description = models.TextField()

    prep_time = models.IntegerField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, null=True)

    likes = models.IntegerField(default=0, blank=True, editable=False)
    dislikes = models.IntegerField(default=0, blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)


# for now, it is not editable
class Comment(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="comments")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(editable=False)

    likes = models.IntegerField(default=0, blank=True, editable=False)
    dislikes = models.IntegerField(default=0, blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
