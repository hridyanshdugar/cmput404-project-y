from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from backend.tests import printFailed, printPassed
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
        print("Testing get user......", end="")
        try:
            response = self.client.get(f"/api/users/{self.user['id']}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            printFailed()
        else:
            printPassed()

    def testGetUserId(self):
        print("Testing get userid.......", end="")
        try:
            response = self.client.get(f"/api/users/a")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            printFailed()
        else:
            printPassed()

    def testPostUser(self):
        print("Testing post user.........", end="")
        try:
            response = self.client.post(f"/api/users/{self.user['id']}", {"displayName": "testNew@displayName.com"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            printFailed()
        else:
            printPassed()

    def testDeleteUser(self):
        print("Testing delete user......", end="")
        try:
            response = self.client.delete(f"/api/users/{self.user['id']}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            printFailed()
        else:
            printPassed()

    def testDeleteUserNone(self):
        print("Testing delete user none......", end="")
        try:
            response = self.client.delete(f"/api/users/{self.user['id']}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.delete(f"/api/users/{self.user['id']}")
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        except:
            printFailed()
        else:
            printPassed()

    def testGetAllUsers(self):
        print("Testing get all users......", end="")
        try:
            response = self.client.get(f"/api/users/")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(len(response.data), 0)
        except:
            printFailed()
        else:
            printPassed()
    
    def testCreateUser(self):
        print("Testing create user", end="")
        try:
            response = self.client.post(f"/api/users/", {"displayName": "test3@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.get(f"/api/users/")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(len(response.data), 0)
        except:
            printFailed()
        else:
            printPassed()

    def testUpdateUser(self):
        print("Testing update user......", end="")
        try:
            response = self.client.put(f"/api/users/{self.user['id']}", {"displayName": "updatedDisplayName"})
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
        except:
            printFailed()
        else:
            printPassed()

    def testInvalidEndpoint(self):
        print("Testing invalid endpoint......", end="")
        try:
            response = self.client.get("/api/invalid_endpoint/")
            self.assertIn(response.status_code, [status.HTTP_404_NOT_FOUND])
        except:
            printFailed()
        else:
            printPassed()

    def testUnauthorizedAccess(self):
        print("Testing unauthorized access......", end="")
        try:
            response = self.client.post("/api/private_data/")
            self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED])
        except:
            printFailed()
        else:
            printPassed()

    def testInternalServerError(self):
        print("Testing internal server error......", end="")
        try:
            response = self.client.post("/api/internal_error/")
            self.assertIn(response.status_code, [status.HTTP_500_INTERNAL_SERVER_ERROR])
        except:
            printFailed()
        else:
            printPassed()

    def testBadRequest(self):
        print("Testing bad request......", end="")
        try:
            response = self.client.post("/api/users/", {})  # Sending empty data intentionally for a bad request
            self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST])
        except:
            printFailed()
        else:
            printPassed()