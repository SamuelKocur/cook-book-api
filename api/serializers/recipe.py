from rest_framework import serializers

from api.models import Instruction, Ingredient, Recipe, AccountFavoriteRecipe, ShoppingListItem, Review


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
    inShoppingList = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = ModelListSerializer
        model = Ingredient
        fields = (
            'id',
            'name',
            'amount',
            'unit',
            'note',
            'inShoppingList',
        )

    def get_inShoppingList(self, obj):
        account_id = self.context.get("account_id")
        if account_id:
            try:
                ShoppingListItem.objects.get(account_id=account_id, ingredient_id=obj.id)
            except ShoppingListItem.DoesNotExist:
                return False

            return True
        return False

    def create(self, validated_data, **kwargs):
        return Ingredient.objects.create(recipe=kwargs.get('recipe'), **validated_data)


class InstructionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    order = serializers.IntegerField(required=False)

    class Meta:
        list_serializer_class = ModelListSerializer
        model = Instruction
        fields = ('id', 'order', 'instruction')

    def create(self, validated_data, **kwargs):
        return Instruction.objects.create(recipe=kwargs.get('recipe'), **validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = ModelListSerializer
        model = Review
        fields = (
            'id',
            'username',
            'rating',
            'text',
            'likes',
            'dislikes',
            'date_created',
        )

    def get_username(self, obj):
        return obj.account.username

    def get_date_created(self, obj):
        return obj.date_created.strftime("%b %d, %Y")

    def validate(self, data):
        if data['rating'] not in (1, 6):
            raise serializers.ValidationError("Ratting is not in range 1-5")

        return data


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    tags = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_tags(self, obj):
        return obj.tags

    def get_rating(self, obj):
        return obj.rating

    def get_username(self, obj):
        return obj.account.username

    def get_liked(self, obj):
        account_id = self.context.get("account_id")
        if account_id:
            try:
                AccountFavoriteRecipe.objects.get(account_id=account_id, recipe_id=obj.id)
            except AccountFavoriteRecipe.DoesNotExist:
                return False

            return True
        return False

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        directions_data = validated_data.pop('instructions')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)

        for direction_data in directions_data:
            Instruction.objects.create(recipe=recipe, **direction_data)

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
