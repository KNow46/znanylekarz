from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from api.models import Doctor, CustomToken, Patient


def getUser(authToken):
    user = CustomToken.objects.get(token=authToken).user

    if isinstance(user, Doctor):
        print('Doctor')
    elif isinstance(user, Patient):
        print('Patient')
    else:
        print('Unknown')

    return user.id

class IsDoctor(BasePermission):

    def has_permission(self, request, view):
        auth_token = request.COOKIES.get('authToken')
        userId = getUser(auth_token)
        print(userId)
        try:
            Doctor.objects.get(id=userId)
            return True
        except Doctor.DoesNotExist:

            return False


