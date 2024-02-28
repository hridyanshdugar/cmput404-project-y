from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class PostTestCase(APITestCase):
    def setUp(self):
        response = self.client.post(f"/auth/signup", {"email": "test@email.com", "password": "test"})
        self.user = response.data["user"]
        self.auth = response.data["auth"]
        response = self.client.post(f"/auth/signup", {"email": "test2@email.com", "password": "test"})
        self.user2 = response.data["user"]
        self.auth2 = response.data["auth"]

    ############################
    # tests
    ############################
    def testGetAllPosts(self):
        response = self.client.get(f"/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def testCreatePostNoAuthor(self):
        response = self.client.post(
            f"/posts/", {"content": "This is a test post"}
        )
        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testCreatePostWithAuthor(self):
        response = self.client.post(
            f"/posts/", {"content": "This is a test post", "author": self.user["id"]}
        )
        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateGoodPost(self):
        response = self.client.post(
            f"/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}
        )
        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def testDeletePost(self):
        response = self.client.post(
            f"/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}
        )
        postId = response.data["id"]
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.auth['access']}"
        }
        response = self.client.delete(f"/posts/{postId}", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testDeletePostUnauthorized(self):
        response = self.client.post(
            f"/posts/", {"content": "This is a test post", "author": self.user["id"], "contentType": "text/plain"}
        )
        postId = response.data["id"]
        headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.auth2['access']}"
        }
        response = self.client.delete(f"/posts/{postId}", **headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
