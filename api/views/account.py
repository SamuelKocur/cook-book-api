from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Account
from api.serializers.account import RegisterSerializer


class SignUpView(APIView):
    """
    Create new user
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    """
    Authenticate user
    """
    def post(self, request):
        data = {
            'email': str(request.data['email']),
            'password': str(request.data['password']),
        }

        try:
            account = Account.objects.get(email=data['email'])
        except Account.DoesNotExist:
            content = {"error": "Invalid email"}
            return Response(content, status.HTTP_400_BAD_REQUEST)

        if account.password == data['password']:
            content = {"id": account.id, "email": account.email}
            return Response(content, status.HTTP_200_OK)

        content = {"error": "Password is incorrect"}
        return Response(content, status.HTTP_401_UNAUTHORIZED)
