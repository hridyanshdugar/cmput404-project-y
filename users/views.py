import uuid
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, AuthorSerializer, RemoteUserSerializer, download_image
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import requests
from requests.exceptions import JSONDecodeError
from django.core.files.base import ContentFile
from rest_framework.pagination import PageNumberPagination
from nodes.models import Node
from nodes.views import is_basicAuth, basicAuth
from requests.auth import HTTPBasicAuth

class Pager(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'

def download_profile(instance, url):
    response = requests.get(url)
    if response.status_code == 200:
        instance.profileImage.save(name=f"pfp_{uuid.uuid4()}.jpg", content=ContentFile(response.content), save=True)
        return True
    return False

def download_profileBack(instance, url):
    response = requests.get(url)
    if response.status_code == 200:
        instance.profileBackgroundImage.save(name=f"pfp_{uuid.uuid4()}.jpg", content=ContentFile(response.content), save=True)
        return True
    return False

class AllUsersViewPK(APIView):

    def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')

    
    def get(self, request,pk):
        user_auth = get_object_or_404(Node,is_self=True).username
        pass_auth = get_object_or_404(Node,is_self=True).password
        response = None
        if User.objects.filter(id=pk, host=Node.objects.get(is_self=True).url).exists():
            user = User.objects.get(id=pk)
            serializer = AuthorSerializer(user,context={'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            for node in Node.objects.filter(is_self=False):
                print(node.url + "api/users/" + str(pk))
                try:
                    response = requests.get(node.url + "api/users/" + str(pk), timeout=3, auth=HTTPBasicAuth(user_auth, pass_auth))
                    
                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                            print(response_data, node.url)
                            
                            if node.url == response_data["host"]:
                                hasPfp = False
                                hasPfpBack = False
                                if "profileImage" in response_data:
                                    hasPfp = response_data.pop("profileImage")
                                if "profileBackgroundImage" in response_data:
                                    hasPfpBack = response_data.pop("profileBackgroundImage")
                                print(response_data)
                                user = None
                                serializer = None
                                try:
                                    user = User.objects.get(id=pk)
                                    serializer = RemoteUserSerializer(user,data=response_data,partial=True)
                                except Exception as e:
                                    print(e)                              
                                    serializer = RemoteUserSerializer(data=response_data)
                                if serializer.is_valid():
                                    user = serializer.save()
                                    if hasPfp:
                                        download_profile(user, hasPfp)
                                        response_data['profileImage'] = hasPfp
                                    if hasPfpBack:
                                        download_profileBack(user, hasPfpBack)
                                        response_data['profileBackgroundImage'] = hasPfpBack
                                    user = User.objects.get(id=pk)
                                    serializer = AuthorSerializer(user)
                                    return Response(serializer.data, status = status.HTTP_200_OK)
                                else:
                                    print(f"Invalid data from {node.url}: {serializer.errors}")
                                return JsonResponse(response_data)
                        except JSONDecodeError:
                            print(f"Invalid JSON response from {node.url}: {response.text}")
                    else:
                        print(f"Request to {node.url} failed with status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Request to {node.url} failed: {e}")
        return Response({"title": "No User Found", "message": "No user found"}, status = status.HTTP_400_BAD_REQUEST)

class UsersViewPK(APIView):

    def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')


    '''
    GET /users/id
    '''
    def get(self, request,pk):
        # I am getting a 403 error if I send a request to the server with basicauth how to fix this?
        
        user = get_object_or_404(User,id=pk)
        serializer = AuthorSerializer(user,context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    '''
    POST /users
    '''
    def post(self, request,pk):
        user = get_object_or_404(User,id=pk)
        serializer = UserSerializer(user,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST) # Need to change the error message
    '''
    delete /users
    '''
    def delete(self, request,pk):
        user = get_object_or_404(User,id=pk)
        user.delete()
        return Response({"title": "Successfully Deleted", "message": "User was deleted"}, status = status.HTTP_200_OK)

class UsersView(APIView):
     
     def perform_authentication(self, request):
        if is_basicAuth(request):
            if not basicAuth(request):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'HTTP_AUTHORIZATION' in request.META:
            request.META.pop('HTTP_AUTHORIZATION')

    
     pagination = Pager()
     '''
     GET /users
     '''
     def get(self, request):
        try:
            users = User.objects.filter(approved=True, host=Node.objects.get(is_self=True).url)
        except:
            pass
        page_number = request.GET.get('page') or 1
        try:
            page = self.pagination.paginate_queryset(users, request, view=self)
        except:
            page = None
        serializer = AuthorSerializer(page,many=True,context={'request': request})
        if page is not None:
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

     '''
     POST /users
     '''
     def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response({"title": "Invalid Fields", "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        
class AllUsersView(APIView):
    pagination = Pager()
    
    def get(self, request):
        user_auth = get_object_or_404(Node,is_self=True).username
        pass_auth = get_object_or_404(Node,is_self=True).password
        nodes = Node.objects.filter(is_self=False)

        users = User.objects.filter(approved=True)
        serializer = AuthorSerializer(users,many=True,context={'request': request})
        node_responses = serializer.data

        for node in nodes:
            print(node.url + "api/users/")
            try:
                response = requests.get(node.url + "api/users/", timeout=3,auth=HTTPBasicAuth(user_auth, pass_auth))
                
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        print(response_data)
                        node_responses.extend(response_data)
                    except JSONDecodeError:
                        print(f"Invalid JSON response from {node.url}: {response.text}")
                else:
                    print(f"Request to {node.url} failed with status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request to {node.url} failed: {e}")

        page_number = request.GET.get('page') or 1

        page = self.pagination.paginate_queryset(node_responses, request, view=self)
        if page is not None:
            return Response(page, status=status.HTTP_200_OK)
        else:
            # Adjusted to prevent ReferenceError if `page` is None
            return Response({"error": "Bad request or empty page."}, status=status.HTTP_400_BAD_REQUEST)
