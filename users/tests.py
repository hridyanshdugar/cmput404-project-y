from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from users.models import User
# Create your tests here.
class UsersTestCase(APITestCase):
    def setUp(self):
        password = make_password("test")
        self.user = User.objects.create(displayName="test@displayName.com", password=password, approved=True)
        response = self.client.post(f"/api/auth/login", {"displayName": "test@displayName.com", "password": "test"})
        self.user = response.data["user"]
        self.auth = response.data["auth"]
        self.user2 = User.objects.create(displayName="test2@displayName.com", password=password, approved=True)
        response = self.client.post(f"/api/auth/login", {"displayName": "test2@displayName.com", "password": "test"})
        self.user2 = response.data["user"]
        self.auth2 = response.data["auth"]

    def testGetUser(self):
        response = self.client.get(f"/api/users/{self.user['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testGetUserId(self):
        response = self.client.get(f"/api/users/a")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testPostUser(self):
        response = self.client.post(f"/api/users/{self.user['id']}", {"displayName": "testNew@displayName.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDeleteUser(self):
        response = self.client.delete(f"/api/users/{self.user['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDeleteUserNone(self):
        response = self.client.delete(f"/api/users/{self.user['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(f"/api/users/{self.user['id']}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testGetAllUsers(self):
        response = self.client.get(f"/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def testCreateUser(self):
        response = self.client.post(f"/api/users/", {"displayName": "test3@displayName.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)