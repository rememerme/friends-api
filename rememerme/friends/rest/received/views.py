from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.received.forms import FriendsGetListForm, FriendsPostForm, FriendsPutForm, FriendsGetSingleForm
from rememerme.friends.rest.received.exceptions import BadRequestException, NotImplementedException

class ReceivedListView(APIView):
    '''
       Used for searching by properties or listing all friends available.
    '''
    
    def get(self, request):
        '''
            Used to get all friends of a user
        '''
        # get the offset and limit query parameters
        form = FriendsGetListForm(request.QUERY_PARAMS)
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
        
class ReceivedSingleView(APIView):
    '''
       Used for managing user properties, getting specific users and deleting users.
    '''
    
    def get(self, request, user_id):
        '''
            Used to get a user by id.
        '''
        # get the offset and limit query parameters
        form = FriendsGetSingleForm({ 'user_id' : user_id })
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            
    
    def put(self, request, user_id):
        '''
            Used to update fields for a given user.
        '''
        data = { key : request.DATA[key] for key in request.DATA }
        data['user_id'] = user_id
        form = FriendsPutForm(data)

        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
        
    def delete(self, request, user_id):
        '''
            Used to delete a user making it inactive.
        '''
        raise NotImplementedException()
