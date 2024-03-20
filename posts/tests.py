from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from users.models import User

class PostTestCase(APITestCase):
    def setUp(self):
        password = make_password("test")
        self.user = User.objects.create(email="test@email.com", password=password, approved=True)
        response = self.client.post(f"/api/auth/login", {"email": "test@email.com", "password": "test"})
        self.user = response.data["user"]
        self.auth = response.data["auth"]["access"]
        self.user2 = User.objects.create(email="test2@email.com", password=password, approved=True)
        response = self.client.post(f"/api/auth/login", {"email": "test2@email.com", "password": "test"})
        self.user2 = response.data["user"]
        self.auth2 = response.data["auth"]["access"]

    ############################
    # tests
    ############################
    def testGetAllPosts(self):
        response = self.client.get(f"/api/posts/", **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def testCreatePostNoAuthor(self):
        response = self.client.post(
            f"/api/posts/", {"content": "This is a test post"}
        )
        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testCreatePostWithAuthor(self):
        response = self.client.post(
            f"/api/posts/", {"content": "This is a test post", "author": self.user["id"]}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}
        )
        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateGoodPost(self):
        response = self.client.post(
            f"/api/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}
        )
        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/api/posts/", **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def testDeletePost(self):
        response = self.client.post(
            f"/api/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}
        )
        postId = response.data["id"]
        response = self.client.delete(f"/api/posts/{postId}", **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDeletePostUnauthorized(self):
        response = self.client.post(
            f"/api/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}
        )
        postId = response.data["id"]
        response = self.client.delete(f"/api/posts/{postId}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
