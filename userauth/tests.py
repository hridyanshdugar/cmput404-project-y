from rest_framework import status
from rest_framework.test import APITestCase
from backend.tests import printFailed, printPassed
# Create your tests here.
class AuthTestCase(APITestCase):
    def testSingup(self):
        try:
            print("Testing sign up........", end="")
            response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            printFailed()
        else:
            printPassed()

    def testDuplicatedisplayName(self):
        print("Testing duplicate display name.....", end="")
        try:
            response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()

    def testNoPassword(self):
        print("Testing no password.....", end="")
        try:
            response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()

    def testNodisplayName(self):
        print("Testing no display name.....", end="")
        try:
            response = self.client.post(f"/api/auth/signup", {"password": "test"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()
    
    def testLogin(self):
        try:
            print("Testing login.....", end="")
            response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.post(f"/api/auth/login", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()
        

    def testLoginNoPassword(self):
        try:
            print("Testing login no password", end="")
            response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.post(f"/api/auth/login", {"displayName": "test@displayName.com"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()

    def testLoginNodisplayName(self):
        try:
            print("Testing login no display name", end="")
            response = self.client.post(f"/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.post(f"/api/auth/login", {"password": "test"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()
    
    def testChangePassword(self):
        try:
            print("Testing change password.....", end="")
            response = self.client.post("/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            token = response.data.get('token', '')
            
            # Change password
            response = self.client.put("/api/auth/password/", {"old_password": "test", "new_password": "newpassword"}, HTTP_AUTHORIZATION=f'Bearer {token}')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Login with new password
            response = self.client.post("/api/auth/login", {"displayName": "test@displayName.com", "password": "newpassword"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            printFailed()
        else:
            printPassed()

    def testChangePasswordNoToken(self):
        try:
            print("Testing change password without token.....", end="")
            response = self.client.put("/api/auth/password/", {"old_password": "test", "new_password": "newpassword"})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        except:
            printFailed()
        else:
            printPassed()

    def testChangePasswordInvalidToken(self):
        try:
            print("Testing change password with invalid token.....", end="")
            response = self.client.put("/api/auth/password/", {"old_password": "test", "new_password": "newpassword"}, HTTP_AUTHORIZATION='Bearer invalidtoken')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        except:
            printFailed()
        else:
            printPassed()

    def testChangePasswordInvalidOldPassword(self):
        try:
            print("Testing change password with invalid old password.....", end="")
            response = self.client.post("/api/auth/signup", {"displayName": "test@displayName.com", "password": "test"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            token = response.data.get('token', '')
            
            # Change password with invalid old password
            response = self.client.put("/api/auth/password/", {"old_password": "invalidpassword", "new_password": "newpassword"}, HTTP_AUTHORIZATION=f'Bearer {token}')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()
