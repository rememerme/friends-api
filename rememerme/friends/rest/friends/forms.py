'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for friends.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin, Jake Gregg 
'''
from django import forms
from config.util import getLimit
import bcrypt
from rememerme.friends.models import Friends
from rememerme.users.models import User
from config import util
from rememerme.friends.rest.exceptions import FriendsListNotFoundException
from rememerme.friends.serializers import FriendsSerializer
from rememerme.users.serializers import UserSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

'''
    Submits this form and returns the friends of the currrent user.
        
    @return: The friends matching the query with the given offset/limit
'''        
class FriendsGetListForm(forms.Form):
    user_id = forms.CharField(required=True)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        # remove the parameters from the cleaned data if they are empty
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise UserNotFoundException()
        return self.cleaned_data
    
    '''
        Submits this form to retrieve the correct information requested by the user.
        Searches by user_id
        
        @return: A list of friends with the given offset/limit
    '''
    def submit(self):
        
        try:
            ans = Friends.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsListNotFoundException()
        except CassaNotFoundException:
            raise FriendListNotFoundException()

        return FriendsSerializer(ans).data

'''
    Submits this form and returns a friend of the currrent user.
        
    @return: The user matching the query
'''         
class FriendsGetSingleForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise UserNotFoundException()
    
    '''
        Submits a form to retrieve a user given the user_id.
        
        @return: A user with the given user_id
    '''
    def submit(self):
        try:
            ans = User.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsListNotFoundException()
        except CassaNotFoundException:
            raise FriendsListNotFoundException()

        return UserSerializer(ans).data
    
class FriendsDeleteForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise UserNotFoundException()
    
    '''
        Submits a form to retrieve a user given the user_id.
        
        @return: A user with the given user_id
    '''
    def submit(self):
        try:
            ans = Friends.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsNotFoundException()
        except CassaNotFoundException:
            raise FriendNotFoundException()

        return FriendsSerializer(ans).data