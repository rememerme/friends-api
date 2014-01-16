'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for users.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin, Jake Gregg 
'''
from django import forms
from config.util import getLimit
import bcrypt
from rememerme.friends.models import Friends
from rememerme.users.models import User
from config import util
from rememerme.friends.rest.friends.exceptions import FriendConflictException, FriendNotFoundException
from rememerme.friends.serializers import FriendsSerializer
from rememerme.users.serializers import UserSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

'''
    Submits this form and returns the friends of the currrent user.
        
    @return: The friends matching the query with the given offset/limit
'''        
class FriendsGetListForm(forms.Form):
    page = forms.CharField(required=False)
    limit = forms.IntegerField(required=False)
    user_id = forms.CharField(required=True)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        self.cleaned_data['limit'] = getLimit(self.cleaned_data)
        self.cleaned_data['page'] = None if not self.cleaned_data['page'] else self.cleaned_data['page']
        # remove the parameters from the cleaned data if they are empty
        
        return self.cleaned_data
    
    '''
        Submits this form to retrieve the correct information requested by the user.
        Searches by user_id
        
        @return: A list of friends with the given offset/limit
    '''
    def submit(self):
        
        ans = Friends.all(page=self.cleaned_data['page'], limit=self.cleaned_data['limit'])
        fResponse = FriendsSerializer(ans, many=True).data
        response = { 'data' : fResponse }
        if ans:
            response['next'] = ans[-1].user_id
        return response

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
            raise FriendNotFoundException()
    
    '''
        Submits a form to retrieve a user given the user_id.
        
        @return: A user with the given user_id
    '''
    def submit(self):
        try:
            ans = User.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsNotFoundException()
        except CassaNotFoundException:
            raise FriendNotFoundException()

        return UserSerializer(ans).data
    
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
    def submit(self):
        try:
            ans = Friends.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsNotFoundException()
        except CassaNotFoundException:
            raise FriendNotFoundException()

        return FriendsSerializer(ans).data