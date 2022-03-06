from rest_framework import serializers

# from django.contrib.auth.password_validation import validate_password

from cookbook_api.models import Account


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)  # validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields did not match."})

        return data

    def create(self, validated_data):
        account = Account.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password1']
        )

        return account
