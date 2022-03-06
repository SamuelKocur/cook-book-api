from api.models import Recipe


def filter_recipes(content):
    category = content.get('category', None)
    ingredients = content.get('ingredients', None)

    recipes = []

    if ingredients:
        # check for recipes which contains first ingredient
        recs = Recipe.objects.filter(ingredients__name__contains=ingredients[0])
        rec_final = []

        contains_all = False
        for recipe in recs:
            # check if recipe contains all ingredients
            for ingredient in ingredients:
                if recipe.ingredients.filter(name__contains=ingredient):
                    contains_all = True
                else:
                    contains_all = False
                    break

            if contains_all:
                rec_final.append(recipe)

        recipes += rec_final

    if category:
        recipes = list(filter(lambda x: x.category == category, recipes))

    return recipes
