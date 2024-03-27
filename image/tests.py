from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Image
from .views import ImageViewPK, ImageView
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from backend.tests import printFailed, printPassed

class ImageTestCase(APITestCase):
    def setUp(self):
        self.image = Image.objects.create(image='test_image.jpg')

    def testGetImage(self):
        print("Testing get image.......", end="")
        try:
            response = self.client.get(f"/api/images/{self.image.pk}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            printFailed()
        else:
            printPassed()

    def testUpdateImage(self):
        print("Testing update image......", end="")
        try:
            response = self.client.post(f"/api/images/", {'image': 'new_image.jpg'})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()

    def testDeleteImage(self):
        print("Testing delete image.......", end="")
        try:
            response = self.client.delete(f"/api/images/{self.image.pk}")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        except:
            printFailed()
        else:
            printPassed()

    def testPost(self):
        print("Testing post image.......", end="")
        try:
            response= self.client.post("/api/images/", {'image': 'new_image.jpg'})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            printFailed()
        else:
            printPassed()
    
    def testGetNonExistentImage(self):
        print("Testing get non-existent image.......", end="")
        try:
            response = self.client.get("/api/images/1000")  # Assuming 1000 is a non-existent image ID
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        except:
            printFailed()
        else:
            printPassed()

    def testUpdateNonExistentImage(self):
        print("Testing update non-existent image.......", end="")
        try:
            response = self.client.put("/api/images/1000", {'image': 'new_image.jpg'})  # Assuming 1000 is a non-existent image ID
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        except:
            printFailed()
        else:
            printPassed()

    def testDeleteNonExistentImage(self):
        print("Testing delete non-existent image.......", end="")
        try:
            response = self.client.delete("/api/images/1000")  # Assuming 1000 is a non-existent image ID
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        except:
            printFailed()
        else:
            printPassed()

    def testUnauthorizedUpdate(self):
        print("Testing unauthorized update......", end="")
        try:
            response = self.client.put(f"/api/images/{self.image.pk}", {'image': 'new_image.jpg'})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        except:
            printFailed()
        else:
            printPassed()

    def testImageUpload(self):
        print("Testing image upload.......", end="")
        try:
            with open('test_image.jpg', 'rb') as file:
                response = self.client.post("/api/images/", {'image': file}, format='multipart')
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        except:
            printFailed()
        else:
            printPassed()