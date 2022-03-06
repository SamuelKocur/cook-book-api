import json

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from cookbook_api.models import Recipe, Ingredient
from cookbook_api.serializers.recipe import RecipeSerializer
from cookbook_api.service.recipe import filter_recipes


class RecipeListView(APIView):
    """
    List recent snippets or create new recipe
    """
    def get(self, request):
        recipes = Recipe.objects.order_by('date_created', 'likes')
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request, **kwargs):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailView(APIView):
    """
    Retrieve, update or delete recipe
    """
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipeListView(APIView):
    """
    Retrieve account' favorite recipes
    """
    def get(self, request, account_id):
        pass


class RecipeFilterListView(APIView):
    """
    Retrieve filtered recipe - by category, by ingredients
    """
    def get(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        recipes = filter_recipes(body)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
