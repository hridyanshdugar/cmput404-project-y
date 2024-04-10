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
    """
    This is the login endpoint
    """
    # print(request.data)
    if 'password' not in request.data or 'displayName' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'title': 'Missing Fields','message': 'A password and displayName is required for logging in'})
    user = User.objects.filter(displayName=request.data['displayName'],approved=True).first()
    inbox = Inbox.objects.get_or_create(author=user)[0]
    inbox.save()
    print("login user", user)
    if not user:
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'title': 'Non-Existant Account','message': 'No account with this displayName exists'})
    input_password = request.data['password']
    stored_password_hash = user.password

    if check_password(input_password,stored_password_hash):

        refresh = RefreshToken.for_user(user)
        refresh['displayName'] = user.displayName
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
    """
    This is the signup endpoint
    """
    if 'password' not in request.data or 'displayName' not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'title': 'No Password','message': 'A password is required for signing up'})
    if User.objects.filter(displayName=request.data['displayName']).first():
        return Response(status=status.HTTP_400_BAD_REQUEST,data={'title': 'displayName Unavailable','message': 'This displayName is already in use'})
    # print(request.data)
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
