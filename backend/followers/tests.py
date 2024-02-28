from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User
from .models import Follower

class FollowersTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            firstName="Test", 
            lastName="User", 
            bio="Test user", 
            email="test@email.com", 
            url="https://localhost:8000/"
        )
        self.user2 = User.objects.create(
            firstName="Test2",
            lastName="User2",
            bio="Test user2",
            email="test2@email.com",
            url="https://localhost:8000/"
        )
        self.client.force_authenticate(user=self.user)

    ############################
    # Positive tests
    ############################

    def sendFollowRequest(self):
        response = self.client.post("/followers/follow", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def sendUnFollowRequest(self):
        response = self.client.post("/followers/unfollow", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def getNewFollowRequests(self):
        response = self.client.get("/followers/get/new/follow/requests", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json", QUERY_STRING=f"?{self.user.email}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def getFollowers(self):
        response = self.client.get("/followers/get/followers", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json", QUERY_STRING=f"?{self.user.email}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def acceptFollowRequest(self):
        response = self.client.put("accept/follow/request/", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def rejectFollowRequest(self):
        response = self.client.put("decline/follow/request/", {
            "name": self.user.email,
            "follower": self.user2.email,
            "url": self.user.url
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)