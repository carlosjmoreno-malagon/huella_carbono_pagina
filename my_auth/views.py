import cloudinary
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



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    serializer = UserProfileSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT','PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data
    
    # Verificar si la imagen ha sido subida
    profile_picture = request.FILES.get('profile_picture')
    
    if profile_picture:
        if profile_picture.size == 0:
            return Response({"error": "El archivo de imagen está vacío."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "No se recibió ningún archivo de imagen."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Intentar subir la imagen a Cloudinary
        upload_result = cloudinary.uploader.upload(profile_picture)
        image_url = upload_result.get('url')  # Obtener la URL de la imagen subida
        print(f"Imagen subida con éxito: {image_url}")
    except Exception as e:
        return Response({"error": f"Error al subir la imagen a Cloudinary: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Intentar obtener el perfil del usuario
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        # Si no existe el perfil, crearlo
        profile = Profile.objects.create(user=user)

    # Actualizar la URL de la imagen de perfil
    profile.profile_picture = image_url  # Asignar la URL de la imagen a la instancia del perfil
    profile.city = data.get('city', profile.city)
    profile.country = data.get('country', profile.country)
    
    # Guardar los cambios en el perfil
    profile.save()

    # Ahora actualizamos el usuario si es necesario
    user_serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
    if user_serializer.is_valid():
        user_serializer.save()

    return Response({
        'user': user_serializer.data,
        'profile': {
            'profile_picture': profile.profile_picture,  # Devolver la URL de la imagen de perfil
            'city': profile.city,
            'country': profile.country
        }
    }, status=status.HTTP_200_OK)