from django.shortcuts import render
from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers import UserSerializer
from inbox.models import Inbox
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
@authentication_classes([])
@permission_classes((AllowAny,))
def login(request):
    print(request.data)
    if 'password' not in request.data or 'email' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'title': 'Missing Fields','message': 'A password and email is required for logging in'})
    user = User.objects.filter(email=request.data['email'],approved=True).first()
    inbox = Inbox.objects.get_or_create(id=user.id)[0]
    inbox.author = user
    inbox.save()
    if not user:
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'title': 'Non-Existant Account','message': 'No account with this email exists'})
    input_password = request.data['password']
    stored_password_hash = user.password

    if check_password(input_password,stored_password_hash):

        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        access_token = str(refresh.access_token)

        serializer = UserSerializer(user)
        result = {
            'user': serializer.data,
            'auth': {
                'refresh': str(refresh),
                'access': access_token,
                'expires_in': refresh.access_token.lifetime.total_seconds()
            }
        }
        return Response(result, status=status.HTTP_200_OK)
    else:         
        return Response(data={'title': 'Invalid Password', 'message': 'You have entered a wrong password'},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([])
@permission_classes((AllowAny,))
def signup(request):
    if 'password' not in request.data or 'email' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'title': 'No Password','message': 'A password is required for signing up'})
    if User.objects.filter(email=request.data['email']).first():
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'title': 'Email Unavailable','message': 'This email is already in use'})
    print(request.data)
    serializer = UserSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()

        serializer = UserSerializer(user)
        result = {
            'user': serializer.data,
        }
        return Response(result, status=status.HTTP_200_OK)
    else:
        print(serializer.errors)  
        return Response(data={'title': 'Invalid Fields', 'message': 'The fields you have entered were invalid'},status=status.HTTP_400_BAD_REQUEST)
