from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.sent.forms import SentGetListForm, SentGetSingleForm, SentDeleteForm
from rememerme.friends.rest.exceptions import BadRequestException, NotImplementedException

class SentListView(APIView):
    '''
       Used for searching by properties or listing all friends available.
    '''
    
    def get(self, request):
        '''
            Used to get all friends of a user
        '''
        # get the offset and limit query parameters
        form = SentGetListForm(request.QUERY_PARAMS)
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            
        
class FriendsSingleView(APIView):
    '''
       Used for managing user properties, getting specific users and deleting users.
    '''
    
    def get(self, request, user_id):
        '''
            Used to get a user by id.
        '''
        # get the offset and limit query parameters
        form = SentGetSingleForm({ 'user_id' : user_id })
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
        
    def delete(self, request, user_id):
        '''
            Used to delete a user making it inactive.
        '''
        # get the offset and limit query parameters
        form = SentDeleteForm({ 'user_id' : user_id })
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
