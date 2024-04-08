from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RemoteNodeAuthenticated(BasePermission):
  """
  Handles permission requests in regards to a user needing the correct credentials
  """

  def has_permission(self, request, view):
    return hasattr(request, "is_node_authenticated") and request.is_node_authenticated


class RemoteOrSessionAuthenticated(RemoteNodeAuthenticated):
  """
  Handles permission requests in regards to a user needing to be logged in
  or having the correct node credentials
  """

  def has_permission(self, request, view):
    session_authenticated = SessionAuthenticated().has_permission(request, view)
    return super().has_permission(request, view) or session_authenticated

class SessionAuthenticated(BasePermission):
  def has_permission(self, request, view):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    print(f"JWT detected? {str(response != None)}")
    return super().has_permission(request, view) and response != None