from pyramid.security import Allow
from pyramid.security import Everyone

from beerledge.models import User


class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
                (Allow, 'group:user', 'edit'),
                (Allow, 'group:admin', 'admin')]

    def __init__(self, request):
        pass


def GroupFinder(username, request):
    try:
        user = User.objects.get(username=username)
        return user.groups
    except User.DoesNotExist:
        return None
