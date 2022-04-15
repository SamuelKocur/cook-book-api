from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Recipe, Review, Account


class RecipeReviewView(APIView):
    """
    Add or remove review from recipe
    """

    def post(self, request):
        account_id = request.query_params.get("account-id")
        recipe_id = request.query_params.get("recipe-id")
        data = {
            'rating': request.data['rating'],
            'text': str(request.data['text']),
        }
        get_object_or_404(Account, pk=account_id)
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.score += data['rating']
        recipe.voted += 1

        message = 'Review successfully changed'
        try:
            review = Review.objects.get(account_id=account_id, recipe_id=recipe_id)
            recipe.score -= review.rating
            recipe.voted -= 1
            review.delete()
        except Review.DoesNotExist:
            message = 'Review successfully added'

        Review.objects.create(
            account_id=account_id,
            recipe_id=recipe_id,
            rating=data['rating'],
            text=data['text'],
        )
        recipe.save()

        return Response({"message": message}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        account_id = request.query_params.get("account-id", "")
        review_id = request.query_params.get("review-id", "")

        try:
            review = Review.objects.get(account_id=account_id, pk=review_id)
            recipe = review.recipe
            recipe.voted -= 1
            recipe.score -= review.rating
            recipe.save()
            review.delete()
        except Review.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
