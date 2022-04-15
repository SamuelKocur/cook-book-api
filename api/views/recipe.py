import json

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Recipe, Review
from api.serializers.recipe import RecipeSerializer
from api.service.recipe import filter_recipes


class RecipeListView(APIView):
    """
    List recent snippets or create new recipe
    """

    def get(self, request):
        account_id = request.query_params.get("account-id")
        recipes = Recipe.objects.all()[:20]
        serializer = RecipeSerializer(recipes, many=True, context={'account_id': account_id})
        recipes = {"recipes": serializer.data}
        return Response(recipes)

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
        account_id = request.query_params.get("account-id")
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer = RecipeSerializer(recipe, context={'account_id': account_id})
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


class RecipeFilterListView(APIView):
    """
    Retrieve filtered recipe
    User can filer recipes by:
    1. ingredients
    2. author
    3. title
    4. rating
    5. tags
    6. time
    """

    def post(self, request):
        account_id = request.query_params.get("account-id")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        recipes = filter_recipes(body)[:20]
        serializer = RecipeSerializer(recipes, many=True, context={'account_id': account_id})
        recipes = {"recipes": serializer.data}
        return Response(recipes)
