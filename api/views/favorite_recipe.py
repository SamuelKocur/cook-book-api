from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Account, Recipe, AccountFavoriteRecipe
from api.serializers.recipe import RecipeSerializer


class FavoriteRecipeListView(APIView):
    """
    Add, remove, get user favorite recipe
    """

    def get(self, request):
        account_id = request.query_params.get("account-id", "")
        account = get_object_or_404(Account, pk=account_id)

        favorite_recipes = account.favorite_recipes.all()
        recipes = [favorite_recipe.recipe for favorite_recipe in favorite_recipes]

        serializer = RecipeSerializer(recipes, many=True)
        recipes = {"recipes": serializer.data}
        return Response(recipes)

    def post(self, request):
        account_id = request.query_params.get("account-id")
        recipe_id = request.query_params.get("recipe-id")
        get_object_or_404(Account, pk=account_id)
        get_object_or_404(Recipe, pk=recipe_id)

        try:
            AccountFavoriteRecipe.objects.get(account_id=account_id, recipe_id=recipe_id)
        except AccountFavoriteRecipe.DoesNotExist:
            AccountFavoriteRecipe.objects.create(account_id=account_id, recipe_id=recipe_id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        account_id = request.query_params.get("account-id", "")
        recipe_id = request.query_params.get("recipe-id", "")

        try:
            user_favorite_recipe = AccountFavoriteRecipe.objects.get(account_id=account_id, recipe_id=recipe_id)
            user_favorite_recipe.delete()
        except AccountFavoriteRecipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
