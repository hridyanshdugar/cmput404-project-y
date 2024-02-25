from django.shortcuts import render
from rest_framework.views import APIView
from users.serializers import AuthorSerializer
from users.models import User

class FollowersView(APIView):

     '''
     GET /followers/<user_id>/
     '''
     def get(self, request, user_id):
          user = get_object_or_404(AppUser, pk = user_id)
          followers = user.followers

          serializer = AuthorSerializer(followers, many = True)
          return Response({"type":"followers","items":serializer.data}, status = status.HTTP_200_OK)
