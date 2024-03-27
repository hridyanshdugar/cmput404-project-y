from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class AuthTestCase(APITestCase):
    def testSingup(self):
        response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDuplicatedisplayName(self):
        response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testNoPassword(self):
        response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testNodisplayName(self):
        response = self.client.post(f"/api/auth/signup", {"password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testLogin(self):
        response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(f"/api/auth/login", {"displayName": "test@displayName.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testLoginNoPassword(self):
        response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(f"/api/auth/login", {"displayName": "test@displayName.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testLoginNodisplayName(self):
        response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(f"/api/auth/login", {"password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)