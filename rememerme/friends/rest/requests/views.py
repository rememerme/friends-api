from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.requests.forms import RequestsPostForm
from rememerme.friends.rest.exceptions import BadRequestException
from rest_framework.permissions import IsAuthenticated

class RequestsListView(APIView):
    permission_classes = (IsAuthenticated,)
    
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