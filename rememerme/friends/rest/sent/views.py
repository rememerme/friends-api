from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.sent.forms import SentGetListForm, SentGetSingleForm, SentDeleteForm
from rememerme.friends.rest.exceptions import BadRequestException, NotImplementedException

class SentListView(APIView):
    '''
       Used for retrieving all friend requests sent by a user.
    '''
    
    def get(self, request):
        '''
            Used to get all friend requests sent of a user
        '''
        # get the offset and limit query parameters
        form = SentGetListForm(request.QUERY_PARAMS)
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            
        
class SentSingleView(APIView):
    '''
       Used for viewing single friend requests sent or canceling a request.
    '''
    
    def get(self, request, user_id):
        '''
            Get a friend request sent by user_id.
        '''
        # get the offset and limit query parameters
        form = SentGetSingleForm({ 'user_id' : user_id })
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
        
    def delete(self, request, user_id):
        '''
            Cancel a friend request sent to a certain user.
        '''
        # get the offset and limit query parameters
        form = SentDeleteForm({ 'user_id' : user_id })
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
