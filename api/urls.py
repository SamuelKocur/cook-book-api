from django.urls import path
from .views import account, recipe

urlpatterns = [
    path('signup/', account.SignUpView.as_view()),
    path('signin/', account.SignInView.as_view()),

    path('recipes/', recipe.RecipeListView().as_view()),
    path('recipes/<int:recipe_id>/', recipe.RecipeDetailView.as_view()),
    path('recipes/<int:account_id>/favorite', recipe.FavoriteRecipeListView.as_view()),
    path('recipes/filter', recipe.RecipeFilterListView.as_view()),
]
