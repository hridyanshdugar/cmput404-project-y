from rest_framework.permissions import BasePermission, IsAuthenticated

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
    session_authenticated = IsAuthenticated().has_permission(request, view)
    return super().has_permission(request, view) or session_authenticated
