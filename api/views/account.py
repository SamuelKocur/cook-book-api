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
    def get(self, request):
        data = {
            'username': str(request.data['username']),
            'password': str(request.data['password']),
        }

        try:
            account = Account.objects.get(username=data['username'])
        except Account.DoesNotExist:
            content = {'invalid username'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if account.password == data['password']:
            return Response(status=status.HTTP_200_OK)

        content = {'bad password'}
        return Response(content, status.HTTP_401_UNAUTHORIZED)
