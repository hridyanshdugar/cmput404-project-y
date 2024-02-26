import json
from .models import NewFollowRequest, Follower


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

def addToFollowerTable(name, follower, url):
    f = Follower()
    f.name = name
    f.follower = follower
    f.followerUrl = url
    f.save()