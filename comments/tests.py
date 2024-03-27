from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from users.models import User
from posts.models import Post
import json 
from backend.tests import printFailed, printPassed

class PostTestCase(APITestCase):
    def setUp(self):
        password = make_password("test")
        self.user = User.objects.create(displayName="test@displayName.com", password=password, approved=True)
        response = self.client.post(f"/api/auth/login", {"displayName": "test@displayName.com", "password": "test"})
        self.user = response.data["user"]
        self.auth = response.data["auth"]["access"]
        self.user2 = User.objects.create(displayName="test2@displayName.com", password=password, approved=True)
        response = self.client.post(f"/api/auth/login", {"displayName": "test2@displayName.com", "password": "test"})
        self.user2 = response.data["user"]
        self.auth2 = response.data["auth"]["access"]
        self.post = self.client.post(f"/api/authors/{self.user['id']}/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}).data
        self.postId = self.post["id"]

    ############################
    # tests
    ############################
    def testGetAllComments(self):
        print("Testing get all comments.......", end="")
        response = self.client.get(f"/api/posts/${str(self.postId)}/comments/", **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'})
        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            printFailed()
        else:
            printPassed()
