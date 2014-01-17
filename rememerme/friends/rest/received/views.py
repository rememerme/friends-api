from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.received.forms import ReceievedGetListForm, ReceivedPutForm, ReceievedGetSingleForm, ReceivedDeleteForm
from rememerme.friends.rest.exceptions import BadRequestException, NotImplementedException

class ReceivedListView(APIView):
    '''
       Used for searching by properties or listing all friend requests received available.
    '''
    
    def get(self, request):
        '''
            Used to get all friends requests receieved of a user
        '''
        # get the offset and limit query parameters
        form = ReceivedGetListForm(request.QUERY_PARAMS)
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
        
class ReceivedSingleView(APIView):
    '''
       Accepting, denying, and viewing requests received.
    '''
    
    def get(self, request, user_id):
        '''
            Get the request received.
        '''
        # get the offset and limit query parameters
        form = ReceivedGetSingleForm({ 'user_id' : user_id })
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            
    
    def put(self, request, user_id):
        '''
            Accept friend request.
        '''
        data = { key : request.DATA[key] for key in request.DATA }
        data['user_id'] = user_id
        form = ReceivedPutForm(data)

        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
        
    def delete(self, request, user_id):
        '''
            Deny friend request.
        '''
        raise NotImplementedException()
