from rest_framework import serializers

from api.models import ShoppingListItem


class ShoppingListItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingListItem
        fields = (
            'id',
            'name',
            'amount',
        )

    def get_name(self, obj):
        if obj.ingredient is None:
            return obj.name

        return obj.ingredient.name

    def get_amount(self, obj):
        if obj.ingredient is None:
            return obj.amount

        amount = obj.ingredient.amount if obj.ingredient.amount is not None else " "
        unit = obj.ingredient.unit if obj.ingredient.unit is not None else " "
        return amount + " " + unit
