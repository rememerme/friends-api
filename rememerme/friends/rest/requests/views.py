from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.requests.forms import RequestsPostForm
from rememerme.friends.rest.exceptions import BadRequestException

class RequestsListView(APIView):
    '''
       Used for making and viewing friend requests.
    '''            

    def post(self, request):
        '''
            Used to create a new friend request.
        '''
        form = RequestsPostForm(request.DATA)

        if form.is_valid():
            return Response(form.submit(request))
        else:
            raise BadRequestException()