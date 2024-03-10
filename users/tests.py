from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class UsersTestCase(APITestCase):
    def setUp(self):
        response = self.client.post(f"/auth/signup", {"email": "test@email.com", "password": "test"})
        self.user = response.data["user"]
        self.auth = response.data["auth"]
        response = self.client.post(f"/auth/signup", {"email": "test2@email.com", "password": "test"})
        self.user2 = response.data["user"]
        self.auth2 = response.data["auth"]

    def testGetUser(self):
        response = self.client.get(f"/users/{self.user['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testGetUserBadId(self):
        response = self.client.get(f"/users/BLAH")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testPostUser(self):
        response = self.client.post(f"/users/{self.user['id']}", {"email": "testNew@email.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDeleteUser(self):
        response = self.client.delete(f"/users/{self.user['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDeleteUserNone(self):
        response = self.client.delete(f"/users/{self.user['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(f"/users/{self.user['id']}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testGetAllUsers(self):
        response = self.client.get(f"/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def testCreateUser(self):
        response = self.client.post(f"/users/", {"email": "test3@email.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)