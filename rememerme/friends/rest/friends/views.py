from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.friends.forms import FriendsGetListForm, FriendsGetSingleForm
from rememerme.friends.rest.exceptions import BadRequestException, NotImplementedException

class FriendsListView(APIView):
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
        
class FriendsSingleView(APIView):
    '''
       Used for managing user properties, getting specific users and deleting users.
    '''
    
    def get(self, request, user_id):
        '''
            Looks at a single friend.
        '''
        # get the offset and limit query parameters
        form = FriendsGetSingleForm({ 'user_id' : user_id })
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            
    
    def delete(self, request, user_id):
        '''
            Remove a friend from the user.
        '''
        raise NotImplementedException()
