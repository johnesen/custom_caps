from rest_framework import status
from rest_framework.exceptions import APIException


class BaseException(APIException):
    def __init__(self, detail=None, code=None, status=None):
        if status:
            self.status_code = status
        super().__init__(detail, code)

class UserAlreadyExist(BaseException):
    default_code = 'user_exists'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "user already exists"


class UserNotFound(BaseException):
    default_detail = 'user not found'
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'user_not_found'


class UserNotVerified(BaseException):
    default_detail = 'user not verified'
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'user_not_virified'
