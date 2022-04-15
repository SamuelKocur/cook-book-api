from django.db import models


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="ingredients"
    )
    name = models.CharField(max_length=128)
    amount = models.CharField(max_length=20, null=True)
    unit = models.CharField(max_length=16, null=True, blank=True)
    note = models.TextField(blank=True)


class Instruction(models.Model):
    recipe = models.ForeignKey(
        "Recipe", on_delete=models.CASCADE, related_name="instructions"
    )
    order = models.IntegerField()
    instruction = models.TextField()

    class Meta:
        ordering = ['order']


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

    class Cuisine(models.TextChoices):
        ASIAN = 'asian'
        JAPANESE = 'japanese'
        CHINESE = 'chinese'
        KOREAN = 'korean'
        INDIAN = 'indian'
        SEAFOOD = 'seafood'
        MEXICAN = 'mexican'
        AMERICAN = 'american'
        ITALIAN = 'italian'
        BRITISH = 'british'
        FRENCH = 'french'
        GREEK = 'greek'
        SLOVAK = 'slovak'
        AFRICAN = 'african'

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
    description = models.TextField(null=True)
    cuisine = models.CharField(max_length=20, choices=Cuisine.choices, null=True, blank=True)

    prep_time = models.IntegerField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, null=True)

    vegan = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)
    diary_free = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)
    lacto_free = models.BooleanField(default=False)

    score = models.FloatField(default=0, blank=True)
    voted = models.IntegerField(default=0, blank=True)

    likes = models.IntegerField(default=0, blank=True, editable=False)
    dislikes = models.IntegerField(default=0, blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-date_created']

    @property
    def tags(self):
        tags = [self.category, self.difficulty]

        if self.vegan:
            tags.append("vegan")
        if self.vegetarian:
            tags.append("vegetarian")
        if self.diary_free:
            tags.append("diary free")
        if self.gluten_free:
            tags.append("gluten free")
        if self.lacto_free:
            tags.append("lacto free")

        if self.cuisine:
            tags.append(self.cuisine)

        return tags

    @property
    def rating(self):
        if self.voted == 0:
            return 0
        return round(self.score / self.voted, 2)

    def __str__(self):
        return f"{self.title} {self.id}"


# for now, it is not editable
class Review(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="reviews")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="reviews")
    rating = models.FloatField(default=0)
    text = models.TextField()

    likes = models.IntegerField(default=0, blank=True, editable=False)
    dislikes = models.IntegerField(default=0, blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-date_created']


class AccountFavoriteRecipe(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="favorite_recipes")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="favorite_to")

    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('account', 'recipe',)
        ordering = ['-date_added']
