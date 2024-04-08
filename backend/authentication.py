import base64
from django.conf import settings
from django.http import HttpRequest
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from nodes.models import Node

class RemoteNodeAuthentication(BaseAuthentication):
  def authenticate(self, request: HttpRequest):
    our_node = Node.objects.get(is_self=True)

    ad = get_authorization_header(request).split()
    request.iii = False

    if not ad or ad[0].lower() != b"basic":
      return None
    
    if len(ad) != 2:
      raise exceptions.ParseError("Invalid Sad JWT: :)")
    
    edde = ad[1]
    try:
      adab6 = base64.b64decode(edde).decode("utf-8")
    except:
      raise exceptions.ParseError("Invalid Sad JWT: :}")
    
    cr = adab6.split(":")
    if len(cr) != 2:
      raise exceptions.ParseError("Invalid Sad JWT: :(")
    
    u, p = cr

    if (u != our_node.username) \
      or (p != our_node.password):
        raise exceptions.NotAuthenticated("Invalid Sad JWT: :()")

    print("- asdfdsdfdss")
    request.iii = True
    return (None, None)

  def authenticate_header(self, request):
    return "Basic realm=\"api\""