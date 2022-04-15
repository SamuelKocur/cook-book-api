from django.contrib import admin

from api.models import Account, Instruction, AccountFavoriteRecipe, Ingredient, Recipe, ShoppingListItem


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient
    extra = 1


class DirectionInlineAdmin(admin.TabularInline):
    model = Instruction
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    inlines = (IngredientInlineAdmin, DirectionInlineAdmin)
    readonly_fields = ('likes', 'dislikes')


admin.site.register(Account)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(AccountFavoriteRecipe)
admin.site.register(ShoppingListItem)
