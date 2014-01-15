from rest_framework.exceptions import APIException

'''
    Bad Request Exception.
'''
class BadRequestException(APIException):
    status_code = 400
    detail = "A Bad Request was made for the API. Revise input parameters."

'''
    The username or email already exist for the given user.
'''
class FriendConflictException(APIException):
    status_code = 409
    detail = "The user requested for creation already exists"
    
'''
    The requested user was not found.
'''
class FriendNotFoundException(APIException):
    status_code = 400
    detail = "The user requested does not exist"

'''
    The API method was not implemented yet.
'''
class NotImplementedException(APIException):
    status_code = 400
    detail = "This API method has not been implemented"
