from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User
from .models import Post

class PostTestCase(APITestCase):
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

    def getPost(self):
        response = self.client.get("/posts/49c8f6c0-ddcd-4656-9afc-d02a92dbd24e", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)