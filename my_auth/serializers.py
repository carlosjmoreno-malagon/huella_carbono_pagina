from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile
import cloudinary.uploader

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile_picture = serializers.ImageField(write_only=True,required = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2','profile_picture']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture',None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        if profile_picture:
            upload_result = cloudinary.uploader.upload(profile_picture)
            profile_url = upload_result.get('url')
            Profile.objects.create(user=user, profile_picture=profile_url)
        else:
            Profile.objects.create(user=user)
        return user
    


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims (si necesitas agregar alguna información adicional al token)
        token['username'] = user.username

        return token
