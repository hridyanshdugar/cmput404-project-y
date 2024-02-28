from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Image
from .views import ImageViewPK, ImageView
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

class ImageTestCase(APITestCase):
    def setUp(self):
        self.image = Image.objects.create(image='test_image.jpg')

    def testGetImage(self):
        response = self.client.get(f"/images/{self.image.pk}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testUpdateImage(self):
        response = self.client.post(f"/images/{self.image.pk}", {'image': 'new_image.jpg'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testDeleteImage(self):
        response = self.client.delete(f"/images/{self.image.pk}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testPost(self):
        response= self.client.post("/images/", {'image': 'new_image.jpg'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)