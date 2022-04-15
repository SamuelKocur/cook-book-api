from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Account, Ingredient, ShoppingListItem
from api.serializers.shopping_list import ShoppingListItemSerializer


class ShoppingListView(APIView):
    """
    Add, remove, get shopping list
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


class ShoppingListUserItemView(APIView):

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
        item_id = request.query_params.get("item-id", "")

        try:
            shopping_list_item = ShoppingListItem.objects.get(account_id=account_id, pk=item_id)
            shopping_list_item.delete()
        except ShoppingListItem.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)