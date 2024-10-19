from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileUpdateSerializer, UserProfileUpdateSerializer, UserRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Profile
from .serializers import UserProfileSerializer

@api_view(['POST'])
def login(request):
    # Obtener el username y el password del request
    username = request.data.get('username')
    password = request.data.get('password')

    # Autenticar el usuario
    user = authenticate(username=username, password=password)

    if user is not None:
        # Si la autenticación es correcta, crear un token para el usuario
        token, created = Token.objects.get_or_create(user=user)

        # Serializar los datos del usuario
        serializer = UserRegistrationSerializer(instance=user)

        # Devolver la respuesta con el token y los datos del usuario
        return Response({
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    else:
        # Si la autenticación falla, devolver un error
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Register(request):
    serializers = UserRegistrationSerializer(data= request.data)
    if serializers.is_valid():
        serializers.save()

        user = User.objects.get(username = serializers.data['username'])

        user.save()

        token = Token.objects.create(user=user)
        return Response({'token':token.key,'user':serializers.data}, status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    serializers = UserProfileSerializer(user)

    #return Response("tu estas logeado con: {}".format(request.user),status=status.HTTP_200_OK)
    return Response(serializers.data,status=status.HTTP_200_OK)


@api_view(['PUT','PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    try:
        # Intentar obtener el perfil del usuario
        profile = user.profile
    except Profile.DoesNotExist:
        # Si no existe el perfil, crearlo
        profile = Profile.objects.create(user=user)

    user_serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
    profile_serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)

    if user_serializer.is_valid() and profile_serializer.is_valid():
        user_serializer.save()
        profile_serializer.save()
        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        'user_errors': user_serializer.errors,
        'profile_errors': profile_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
