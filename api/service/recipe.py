import json

from api.models import Recipe

# not optimized TODO get data from database only when it's needed - make request more scalable


def filter_recipes(request):
    ingredients = request.get('ingredients', None)
    author = request.get('author', None)
    title = request.get('title', None)
    ratings = request.get('ratings', None)
    tags = request.get('tags', None)
    time = request.get('time', None)

    recipes = []

    if ingredients:
        recipes = filter_recipe_by_ingredients(recipes, ingredients)
        # check if there was at least one recipe which meets the conditions
        # if yes we continue in filtering
        if len(recipes) == 0:
            return []

    if author:
        recipes = filter_recipe_by_author(recipes, author)
        if len(recipes) == 0:
            return []

    if title:
        recipes = filter_recipe_by_title(recipes, title)
        if len(recipes) == 0:
            return []

    if ratings:
        recipes = filter_recipe_by_rating(recipes, ratings)
        if len(recipes) == 0:
            return []

    if tags:
        recipes = filter_recipe_by_tags(recipes, tags)
        if len(recipes) == 0:
            return []

    if time:
        recipes = filter_by_time(recipes, time)
        if len(recipes) == 0:
            return []

    return recipes


def filter_recipe_by_ingredients(recipes, ingredients):
    if len(recipes) == 0:
        # check for recipes which contains first ingredient
        recipes = Recipe.objects.filter(ingredients__name__contains=ingredients[0])

    recipes_final = []

    for recipe in recipes:
        contains_all = False
        # check if recipe contains all ingredients
        for ingredient in ingredients:
            if recipe.ingredients.filter(name__contains=ingredient):
                contains_all = True
            else:
                contains_all = False
                break

        if contains_all:
            recipes_final.append(recipe)

    return recipes_final


def filter_recipe_by_author(recipes, author):
    if len(recipes) == 0:
        return Recipe.objects.filter(account__username__contains=author)

    recs_ids = [recipe.id for recipe in recipes]
    return Recipe.objects.filter(account__username__contains=author, pk__in=recs_ids)


def filter_recipe_by_title(recipes, title):
    words = title.lower().split(" ")

    if len(recipes) == 0:
        recipes.extend(Recipe.objects.filter(title__icontains=words[0]))

    recipes_final = []
    for recipe in recipes:
        if all(word in recipe.title.lower() for word in words):
            recipes_final.append(recipe)

    return recipes_final


def filter_recipe_by_rating(recipes, ratings):
    if len(recipes) == 0:
        recipes = Recipe.objects.filter()

    return [recipe for recipe in recipes if round(recipe.rating) in ratings]


def filter_recipe_by_tags(recipes, tags):
    if len(recipes) == 0:
        recipes = Recipe.objects.filter()

    recipes_final = []
    for recipe in recipes:
        if all(tag in recipe.tags for tag in tags):
            recipes_final.append(recipe)

    return recipes_final


def filter_by_time(recipes, time):
    if len(recipes) == 0:
        recipes = Recipe.objects.filter()

    return [recipe for recipe in recipes if (recipe.prep_time + recipe.cook_time) <= time]
