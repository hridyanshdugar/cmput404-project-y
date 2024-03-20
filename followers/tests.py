from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User
from .models import Follower

class FollowersTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@email.com", 
            password="test"
        )
        self.user2 = User.objects.create(
            email="test2@email.com",
            password="test"
        )
        self.client.force_authenticate(user=self.user)

    ############################
    # Positive tests
    ############################

    def testsendFollowRequest(self):
        response = self.client.post("/api/followers/follow/", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testsendUnFollowRequest(self):
        response = self.client.post("/api/followers/unfollow/", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testgetNewFollowRequests(self):
        response = self.client.get("/api/followers/get/new/follow/requests", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json", QUERY_STRING=f"?{self.user.email}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testgetFollowers(self):
        response = self.client.get(f"/api/followers/get/followers/${self.user.email}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testacceptFollowRequest(self):
        response = self.client.put("/api/followers/accept/follow/request/", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testrejectFollowRequest(self):
        response = self.client.put("/api/followers/decline/follow/request/", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)