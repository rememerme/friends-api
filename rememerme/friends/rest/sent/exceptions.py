from rest_framework.exceptions import APIException

class BadRequestException(APIException):
    '''
        Bad Request Exception.
    '''
    status_code = 400
    detail = "A Bad Request was made for the API. Revise input parameters."
    
class FriendsListNotFoundException(APIException):
    '''
        The requested user was not found.
    '''
    status_code = 400
    detail = "The user is a total loser and has no friends. Please be more social."

class NotImplementedException(APIException):
    '''
        The API method was not implemented yet.
    '''
    status_code = 400
    detail = "This API method has not been implemented"

class UserNotFoundException(APIException):
    '''
        The user is not part of the system.
    '''
    status_code = 400
    detail = "You are not apparently part of the system."

class RequestsListNotFoundException(APIException):
    '''
        The requested friends list was not found.
    '''
    status_code = 400
    detail = "The user is a total loser and has no friends. Please be more social."