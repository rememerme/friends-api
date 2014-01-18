'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for friends.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin, Jake Gregg 
'''
from django import forms
from rememerme.friends.models import Friends
from rememerme.friends.rest.exceptions import FriendsListNotFoundException, FriendNotFoundException
from rememerme.friends.serializers import FriendsSerializer
from uuid import UUID
from rememerme.users.client import UserClient
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException
import json

'''
    Submits this form and returns the friends of the currrent user.
        
    @return: The friends matching the query with the given offset/limit
'''        
class FriendsGetListForm(forms.Form):
    
    '''
        Submits this form to retrieve the correct information requested by the user.
        Searches by user_id
        
        @return: A list of friends with the given offset/limit
    '''
    def submit(self, request):
        
        try:
            ans = Friends.getByID(request.user.pk)
            if not ans:
                raise FriendsListNotFoundException()
        except CassaNotFoundException:
            raise FriendsListNotFoundException()

        return FriendsSerializer(ans).data

'''
    Submits this form and deletes the friend from the user's friend list.
'''
class FriendsDeleteForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise FriendNotFoundException()
    
    '''
        Submits a form to retrieve a user given the user_id.
        
        @return: A user with the given user_id
    '''
    def submit(self, request):
        try:
            ans = Friends.getByID(request.user.pk)
            if not ans:
                raise FriendNotFoundException()
        except CassaNotFoundException:
            raise FriendNotFoundException()

        friends = json.loads(ans.friends_list)
        del friends[self.cleaned_data['user_id']]
        ans.friends_list = json.dumps(friends)
        ans.save()

        return UserClient(request.auth).get(self.cleaned_data['user_id'])
    
    
    
