import copy
import json
import uuid
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from inbox.views import get_foreign_user
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
from backend.permissions import RemoteOrSessionAuthenticated, SessionAuthenticated

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
    permission_classes = [ SessionAuthenticated ]
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
                print("bigbibibibibigggggggg", node.url + "api/authors/" + str(pk) + "/")
                try:
                    response = requests.get(node.url + "api/authors/" + str(pk) + "/", timeout=3, auth=HTTPBasicAuth(node.username, node.password))
                    
                    if response.status_code == 200:
                        try:
                            response_data = response.json()
                            response_data2 = copy.deepcopy(response.json())
                            print("bob22323232 ", response_data, node.url )
                            
                            response_data["host"] = response_data["host"] if (response_data["host"][-1] == "/") else response_data["host"] + "/"
                            print("bugg22222222", node.url, response_data["host"])
                            if node.url == response_data["host"]:
                                print("bob22323232 1")
                                get_foreign_user(response_data)
                                print("bob22323232 2")
                                return JsonResponse(response_data2)
                        except Exception as e:
                            print(f"I44nvalid JSON response from {node.url}: {response.text} failed: {e}")
                    else:
                        print(f"R33equest to {node.url} failed with status code: {response.status_code}")
                except Exception as e:
                    print(f"R22equest to {node.url} failed: {e}")
        return Response({"title": "No User Found", "message": "No user found"}, status = status.HTTP_400_BAD_REQUEST)

class UsersViewPK(APIView):

    permission_classes = [ RemoteOrSessionAuthenticated ]


    '''
    GET /authors/id
    '''
    def get(self, request,pk):
        # I am getting a 403 error if I send a request to the server with basicauth how to fix this?
        
        user = get_object_or_404(User,id=pk)
        serializer = AuthorSerializer(user,context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    '''
    POST /authors
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
    delete /authors
    '''
    def delete(self, request,pk):
        user = get_object_or_404(User,id=pk)
        user.delete()
        return Response({"title": "Successfully Deleted", "message": "User was deleted"}, status = status.HTTP_200_OK)

class UsersView(APIView):     
     
     permission_classes = [ RemoteOrSessionAuthenticated ]
     pagination = Pager()
     '''
     GET /authors
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
        data = dict()
        data["items"] = serializer.data
        data["type"] = "authors"
        if page is not None:
            return Response(data, status = status.HTTP_200_OK)
        else:
            return Response(data, status = status.HTTP_400_BAD_REQUEST)

     '''
     POST /authors
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
        nodes = Node.objects.filter(is_self=False)

        users = User.objects.filter(approved=True)
        serializer = AuthorSerializer(users,many=True,context={'request': request})
        node_responses = json.loads(json.dumps(serializer.data))

        for node in nodes:
            print(node.url + "api/authors/ ffjjff")
            try:
                response = requests.get(node.url + "api/authors", timeout=3, auth=HTTPBasicAuth(node.username, node.password))
                
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        print(response_data)
                        if "items" in response_data:
                            response_data = response_data["items"]
                        node_responses.extend(response_data)
                    except JSONDecodeError:
                        print(f"Invalid JSON response from {node.url}: {response.text}")
                else:
                    print(f"Request to {node.url} failed with status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request to {node.url} failed: {e}")
        print("elphant 1", node_responses, type(node_responses))
        return Response(node_responses, status = status.HTTP_200_OK)
