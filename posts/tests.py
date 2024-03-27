from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from users.models import User
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

    ############################
    # tests
    ############################
    def testGetAllPosts(self):
        try:
            print("Testing get all posts.......", end="")
            response = self.client.get(f"/api/authors/{self.user['id']}/posts/", **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 0)
        except Exception as e:
            printFailed()
        else:
            printPassed()

    def testCreatePostNoAuthor(self):
        
        # assert
        try:
            print("Testing get all posts.......", end="")
            response = self.client.post(
                f"/api/posts/", {"content": "This is a test post"}
            )
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            printFailed()
        else:
            printPassed()

    def testCreatePostWithAuthor(self):
        

        try:
        # assert
            print("Testing create post with no author.......", end="")
            response = self.client.post(
                f"/api/posts/", {"content": "This is a test post", "author": self.user["id"]}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            printFailed()
        else:
            printPassed()

    def testCreateGoodPost(self):
        
        # assert

        try:
            print("Testing create good post.......", end="")
            response = self.client.post(
                f"/api/authors/{self.user['id']}/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.get(f"/api/posts/", **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
        except Exception as a:
            printFailed()
        else:
            printPassed()

    def testDeletePost(self):
        try:
            print("Test Delete post.........", end="")
            response = self.client.post(
                f"/api/authors/{self.user['id']}/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}
            )
            postId = response.data["id"]
            response = self.client.delete(f"/api/posts/{postId}", **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            printFailed()
        else:
            printPassed()

    def testDeletePostUnauthorized(self):
        try:
            print("Test delete post unauthorized.......", end="")
            response = self.client.post(
                f"/api/authors/{self.user['id']}/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}, **{'HTTP_AUTHORIZATION': f'Bearer {self.auth}'}
            )
            postId = response.data["id"]
            response = self.client.delete(f"/api/posts/{postId}")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            printFailed()
        else:
            printPassed()
