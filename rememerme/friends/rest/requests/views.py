from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.requests.forms import RequestsGetForm, RequestsPostForm
from rememerme.friends.rest.requests.exceptions import BadRequestException, NotImplementedException

class RequestsListView(APIView):
    '''
       Used for making and viewing friend requests.
    '''
    
    def get(self, request):
        '''
            Used to get all friends requests of a user
        '''
        # get the offset and limit query parameters
        form = RequestsGetForm(request.QUERY_PARAMS)
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            

    def post(self, request):
        '''
            Used to create a new friend request.
        '''
        form = RequestsPostForm(request.DATA)

        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()