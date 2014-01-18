from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.sent.forms import SentGetListForm, SentDeleteForm
from rememerme.friends.rest.exceptions import BadRequestException
from rest_framework.permissions import IsAuthenticated

class SentListView(APIView):
    permission_classes = (IsAuthenticated,)
    
    '''
       Used for searching by properties or listing all friend requests received available.
    '''
    
    def get(self, request):
        '''
            Used to get all friends requests receieved of a user
        '''
        # get the offset and limit query parameters
        form = SentGetListForm(request.QUERY_PARAMS)
        
        if form.is_valid():
            return Response(form.submit(request))
        else:
            raise BadRequestException()
        
class SentSingleView(APIView):
    permission_classes = (IsAuthenticated,)
    
    '''
       Accepting, denying, and viewing requests received.
    '''     
    
    def delete(self, request, user_id):
        '''
            Deny friend request.
        '''
        form = SentDeleteForm({ 'user_id' : user_id })

        if form.is_valid():
            return Response(form.submit(request))
        else:
            raise BadRequestException()
