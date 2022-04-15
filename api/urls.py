from django.urls import path
from .views import account, recipe, favorite_recipe, shopping_list

urlpatterns = [
    path('signup/', account.SignUpView.as_view(), name="sign_up"),
    path('signin/', account.SignInView.as_view(), name="sign in"),

    path('recipes/', recipe.RecipeListView().as_view(), name="random_recipes"),
    path('recipes/<int:recipe_id>/', recipe.RecipeDetailView.as_view(), name="recipe_detail"),
    path('recipes/filter/', recipe.RecipeFilterListView.as_view(), name="filtered_recipes"),

    path('recipes/favorite/', favorite_recipe.FavoriteRecipeListView.as_view(), name="user_favorite_recipes"),

    path('shoppinglist/', shopping_list.ShoppingListView.as_view(), name="user_shopping_list"),
    path('shoppinglist/user-item/', shopping_list.ShoppingListUserItemView.as_view(), name="user_own_shopping_list"),
]
