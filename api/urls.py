from django.urls import path
from .views import account, recipe, favorite_recipe, shopping_list, recipe_review

urlpatterns = [
    path('signup/', account.SignUpView.as_view(), name="sign_up"),
    path('signin/', account.SignInView.as_view(), name="sign in"),
    path('account/<int:user_id>/delete', account.DeleteAccountView.as_view(), name="delete_account"),

    path('recipes/', recipe.RecipeListView().as_view(), name="random_recipes"),
    path('recipes/<int:recipe_id>/', recipe.RecipeDetailView.as_view(), name="recipe_detail"),
    path('recipes/filter/', recipe.RecipeFilterListView.as_view(), name="filtered_recipes"),

    path('recipes/favorite/', favorite_recipe.FavoriteRecipeListView.as_view(), name="user_favorite_recipes"),

    path('shoppinglist/ingredient/', shopping_list.ShoppingListIngredientView.as_view()),
    path('shoppinglist/', shopping_list.ShoppingListUserItemListView.as_view()),
    path('shoppinglist/<int:item_id>/', shopping_list.ShoppingListUserItemDetailView.as_view()),

    path('recipes/review/', recipe_review.RecipeReviewView.as_view(), name="add_remove_review")
]
