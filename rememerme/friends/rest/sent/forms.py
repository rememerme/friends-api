'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for friend requests sent.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin
'''
from django import forms
from config.util import getLimit
import bcrypt
from rememerme.friends.models import Friends
from config import util
from rememerme.friends.rest.exceptions import FriendsListNotFoundException, UserNotFoundException, RequestsListNotFoundException
from rememerme.friends.serializers import FriendsSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

'''
    Gets all friend requests sent for a given user.
'''        
class SentGetListForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise UserNotFoundException()
    
    '''
        submits the form and retreives the friend requests sent for a given user.
    '''
    def submit(self):
        try:
            ans = Requests.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise RequestsListNotFoundException()
        except CassaNotFoundException:
            raise RequestsListNotFoundException()

        return RequestsSerializer(ans).data
        
'''
    Gets a single sent friend request for a given user and friend.
'''
class SentGetSingleForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise FriendNotFoundException()
    
    '''
        Submits a form to retrieve a friend request sent for a given user.
        
        @return: the request object.
    '''
    def submit(self):
        try:
            ans = Friends.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsNotFoundException()
        except CassaNotFoundException:
            raise FriendNotFoundException()

        return FriendsSerializer(ans).data
    
'''
    Cancels a friend request for a given user and friend.
'''
class SentDeleteForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise UserNotFoundException()
    
    '''
        Submits a form to cancel a friend request for a given user.
        
        @return: Confirmation of the delete.
    '''
    def submit(self):
        try:
            ans = Friends.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsNotFoundException()
        except CassaNotFoundException:
            raise FriendNotFoundException()

        return FriendsSerializer(ans).data