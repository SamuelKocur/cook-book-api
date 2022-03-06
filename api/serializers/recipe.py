from rest_framework import serializers

from api.models import Direction, Ingredient, Recipe


class ModelListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data, **kwargs):
        model_mapping = {model.id: model for model in instance}

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
        for model_id, data in data_mapping.items():
            model = model_mapping.get(model_id, None)
            if model is None:
                ret.append(self.child.create(data, **kwargs))
            else:
                ret.append(self.child.update(model, data))

        # Perform deletions.
        for model_id, model in model_mapping.items():
            if model_id not in data_mapping:
                model.delete()

        return ret


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    note = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        list_serializer_class = ModelListSerializer
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


class DirectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    order = serializers.IntegerField(required=False)

    class Meta:
        list_serializer_class = ModelListSerializer
        model = Direction
        fields = ('id', 'order', 'direction')

    def create(self, validated_data, **kwargs):
        return Direction.objects.create(recipe=kwargs.get('recipe'), **validated_data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    directions = DirectionSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        directions_data = validated_data.pop('directions')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)

        for direction_data in directions_data:
            Direction.objects.create(recipe=recipe, **direction_data)

        return recipe

    def update(self, instance, validated_data):
        kwargs = {'recipe': instance}

        if 'ingredients' in validated_data:
            nested_serializer = self.fields['ingredients']
            nested_serializer.update(instance.ingredients.all(), validated_data.pop('ingredients'), **kwargs)

        if 'directions' in validated_data:
            nested_serializer = self.fields['directions']
            nested_serializer.update(instance.directions.all(), validated_data.pop('directions'), **kwargs)

        return super(RecipeSerializer, self).update(instance, validated_data)


