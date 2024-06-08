from .models import User, FavoriteCity
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    'email': email,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
        raise serializers.ValidationError('Invalid email or password')


class FavoriteCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCity
        fields = ('id', 'city_name')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    favorite_cities = FavoriteCitySerializer(many=True, read_only=True)  # Add this line

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'favorite_cities')  # Include 'favorite_cities' in fields
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if self.instance:  # If updating existing user, skip unique email validation
            return value

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError({'Password must be atleast 8 characters long and must contain at least one uppercase letter, one lowercase letter, and one special character': list(exc.messages)})
        return value

    def create(self, validated_data):
        favorite_cities_data = validated_data.pop('favorite_cities', [])  # Pop favorite cities data
        user = User.objects.create_user(**validated_data)
        for city_data in favorite_cities_data:
            FavoriteCity.objects.create(user=user, **city_data)  # Create favorite cities for the user
        return user