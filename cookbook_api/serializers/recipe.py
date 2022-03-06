from rest_framework import serializers

from cookbook_api.models import Ingredient, Recipe


class IngredientListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data, **kwargs):
        ingredient_mapping = {ingredient.id: ingredient for ingredient in instance}
        invalid_id = -1
        data_mapping = {}
        for item in validated_data:
            if item.get('id'):
                data_mapping[item.get('id')] = item
            else:
                data_mapping[invalid_id] = item
                invalid_id -= 1

        # Perform creations and updates.
        ret = []
        i = 0
        for ingredient_id, data in data_mapping.items():
            ingredient = ingredient_mapping.get(ingredient_id, None)
            if ingredient is None:
                ret.append(self.child.create(data, **kwargs))
            else:
                ret.append(self.child.update(ingredient, data))

        # Perform deletions.
        for ingredient_id, ingredient in ingredient_mapping.items():
            if ingredient_id not in data_mapping:
                ingredient.delete()
        return ret


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    note = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        list_serializer_class = IngredientListSerializer
        model = Ingredient
        fields = (
            'id',
            'name',
            'amount',
            'unit',
            'note',
        )

    def create(self, validated_data, **kwargs):
        return Ingredient.objects.create(recipe=kwargs.get('recipe'), **validated_data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            nested_serializer = self.fields['ingredients']
            nested_instance = instance.ingredients.all()
            nested_data = validated_data.pop('ingredients')

            kwargs = {'recipe': instance}
            nested_serializer.update(nested_instance, nested_data, **kwargs)

        return super(RecipeSerializer, self).update(instance, validated_data)


