from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Account, Ingredient, ShoppingListItem
from api.serializers.shopping_list import ShoppingListItemSerializer


class ShoppingListIngredientView(APIView):
    """
    Add, remove item to/from shopping list

    Possible to add and remove ingredients from recipes
    """
    def post(self, request):
        account_id = request.query_params.get("account-id")
        ingredient_id = request.query_params.get("ingredient-id")
        get_object_or_404(Account, pk=account_id)
        get_object_or_404(Ingredient, pk=ingredient_id)

        try:
            ShoppingListItem.objects.get(account_id=account_id, ingredient_id=ingredient_id)
        except ShoppingListItem.DoesNotExist:
            ShoppingListItem.objects.create(account_id=account_id, ingredient_id=ingredient_id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        account_id = request.query_params.get("account-id", "")
        ingredient_id = request.query_params.get("ingredient-id", "")

        try:
            shopping_list_item = ShoppingListItem.objects.get(account_id=account_id, ingredient_id=ingredient_id)
            shopping_list_item.delete()
        except ShoppingListItem.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListUserItemListView(APIView):
    """
    Add item to shopping list
    Get shopping list
    Delete all items
    """
    def get(self, request):
        account_id = request.query_params.get("account-id", "")
        account = get_object_or_404(Account, pk=account_id)

        shopping_list_items = account.shopping_list.all()
        serializer = ShoppingListItemSerializer(shopping_list_items, many=True)
        ingredients = {"shoppingListItems": serializer.data}
        return Response(ingredients)

    def post(self, request):
        account_id = request.query_params.get("account-id")
        data = {
            'name': str(request.data['name']),
            'amount': str(request.data['amount']),
        }
        get_object_or_404(Account, pk=account_id)
        ShoppingListItem.objects.create(
            account_id=account_id,
            name=data['name'],
            amount=data['amount'],
        )

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        account_id = request.query_params.get("account-id", "")

        try:
            ShoppingListItem.objects.filter(account_id=account_id).delete()
        except ShoppingListItem.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListUserItemDetailView(APIView):
    """
    Delete item from user shopping list by item_id
    """
    def delete(self, request, item_id):
        account_id = request.query_params.get("account-id", "")

        try:
            ShoppingListItem.objects.get(account_id=account_id, pk=item_id).delete()
        except ShoppingListItem.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
