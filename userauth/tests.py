from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class AuthTestCase(APITestCase):
    def testSingup(self):
        response = self.client.post(f"/auth/signup", {"email": "test@email.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDuplicateEmail(self):
        response = self.client.post(f"/auth/signup", {"email": "test@email.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(f"/auth/signup", {"email": "test@email.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testNoPassword(self):
        response = self.client.post(f"/auth/signup", {"email": "test@email.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testNoEmail(self):
        response = self.client.post(f"/auth/signup", {"password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testLogin(self):
        response = self.client.post(f"/auth/signup", {"email": "test@email.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(f"/auth/login", {"email": "test@email.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testLoginNoPassword(self):
        response = self.client.post(f"/auth/signup", {"email": "test@email.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(f"/auth/login", {"email": "test@email.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testLoginNoEmail(self):
        response = self.client.post(f"/auth/signup", {"email": "test@email.com", "password": "test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(f"/auth/login", {"password": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)