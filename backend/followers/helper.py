import json
from .models import NewFollowRequest


def body_to_json(body):
    bodyUnicode = body.decode('utf-8')
    body = json.loads(bodyUnicode)
    return body

def addToNewFollowRequestTable(body):
    nfr = NewFollowRequest()
    nfr.name = body['name']
    nfr.follower = body['friend']
    nfr.followerUrl = body['url']
    nfr.save()