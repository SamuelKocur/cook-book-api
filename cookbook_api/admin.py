from django.contrib import admin

from cookbook_api.models import Account, Recipe, Ingredient


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    inlines = (IngredientInlineAdmin, )
    readonly_fields = ('likes', 'dislikes')


admin.site.register(Account)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
