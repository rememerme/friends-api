from rest_framework.views import APIView
from rest_framework.response import Response
from rememerme.friends.rest.friends.forms import FriendsGetListForm, FriendsDeleteForm
from rememerme.friends.rest.exceptions import BadRequestException
from rest_framework.permissions import IsAuthenticated

class FriendsListView(APIView):
    permission_classes = (IsAuthenticated,)
    
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
            return Response(form.submit(request))
        else:
            raise BadRequestException()
        
class FriendsSingleView(APIView):
    permission_classes = (IsAuthenticated,)
    
    '''
       Used for looking at a friend and removing friends.
    '''     
    
    def delete(self, request, user_id):
        '''
            Remove a friend from the user.
        '''
        # get the offset and limit query parameters
        form = FriendsDeleteForm({ 'user_id' : user_id })
        
        if form.is_valid():
            return Response(form.submit(request))
        else:
            raise BadRequestException()
