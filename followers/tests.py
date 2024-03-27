import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from users.models import User
from .models import FollowStatus
from backend.tests import printFailed, printPassed

class FollowersTestCase(APITestCase):
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
        self.client.force_authenticate(user=self.user)

    ############################
    # Positive tests
    ############################

    def testsendFollowRequest(self):
        print("Testing send follow request......", end="")
        response = self.client.post(f"/api/authors/{self.user2['id']}/inbox/", {
            "type": "Follow",
            "actor": self.user,
            "object": self.user2
        }, format="json")

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            printFailed()
        else:
            printPassed()

        

    def testsendUnFollowRequest(self):
        print("Testing send unfollow......", end="")
        response = self.client.post(f"/api/authors/{self.user2['id']}/inbox/", {
            "type": "Unfollow",
            "actor": self.user,
            "object": self.user2 
        }, format="json")

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            printFailed()
        else:
            printPassed()

    def testgetFollowers(self):
        print("Testing get followers......", end="")
        response = self.client.get(f"/api/followers/get/followers/{self.user['displayName']}")

        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except Exception as e:
            printFailed()
        else:
            printPassed()

    def testacceptFollowRequest(self):
        print("Testing accept follower request......", end="")
        response = self.client.put("/api/followers/accept/follow/request/", {
            "name": self.user["displayName"],
            "follower": self.user2["displayName"],
            "url": self.user["url"]
        }, format="json")

        try:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            printFailed()
        else:
            printPassed()
    
    def testrejectFollowRequest(self):
        print("Testing reject follower request......", end="")
        response = self.client.put("/api/followers/decline/follow/request/", {
            "name": self.user["displayName"],
            "follower": self.user2["displayName"],
            "url": self.user["url"]
        }, format="json")

        try:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            printFailed()
        else:
            printPassed()