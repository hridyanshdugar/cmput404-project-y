from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RemoteNodeAuthenticated(BasePermission):
  def has_permission(self, request, view):
    return hasattr(request, "iii") and request.iii


class RemoteOrSessionAuthenticated(RemoteNodeAuthenticated):
  def has_permission(self, request, view):
    sa = SessionAuthenticated().has_permission(request, view)
    return super().has_permission(request, view) or sa

class SessionAuthenticated(BasePermission):
  def has_permission(self, request, view):
    aaa = JWTAuthentication()
    response = aaa.authenticate(request)
    print(f"bob detec? {str(response != None)}")
    return super().has_permission(request, view) and response != None