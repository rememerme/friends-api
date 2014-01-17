'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for friend requests received.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin, Jake Gregg
'''
from django import forms
from config.util import getLimit
import bcrypt
from rememerme.friends.models import Requests
from config import util
from rememerme.friends.rest.exceptions import FriendsListNotFoundException, UserNotFoundException, RequestsListNotFoundException
from rememerme.friends.serializers import RequestsSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

'''
    Gets all friend requests recieved and returns them to the user.

    @return: A list of requests matching the query with the given offset/limit
'''        
class ReceivedGetListForm(forms.Form):
    page = forms.CharField(required=False)
    limit = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        self.cleaned_data['limit'] = getLimit(self.cleaned_data)
        self.cleaned_data['page'] = None if not self.cleaned_data['page'] else self.cleaned_data['page']
        # remove the parameters from the cleaned data if they are empty
        if not self.cleaned_data['username']:
            del self.cleaned_data['username']
            
        if not self.cleaned_data['email']:
            del self.cleaned_data['email']
        
        return self.cleaned_data
    
    '''
        Submits the form and returns the friend requests received for the user.
    '''
    def submit(self):
        if 'username' in self.cleaned_data:
            ans = Friends.getByUsername(self.cleaned_data['username'])
            uResponse = FriendsSerializer([] if not ans else [ans], many=True).data
            response = { 'data' : uResponse }
            return response
        elif 'email' in self.cleaned_data:
            ans = Friends.getByEmail(self.cleaned_data['email'])
            uResponse = FriendsSerializer([] if not ans else [ans], many=True).data
            response = { 'data' : uResponse }
            return response
        else:
            ans = Friends.all(page=self.cleaned_data['page'], limit=self.cleaned_data['limit'])
            uResponse = FriendsSerializer(ans, many=True).data
            response = { 'data' : uResponse }
            if ans:
                response['next'] = ans[-1].user_id
            return response

'''
    Gets a single friend request received for the user.
'''     
class ReceivedGetSingleForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise FriendNotFoundException()
    
    '''
        Submits a form to retrieve the friend request received.
        
        @return: The friend request received.
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
    Accepts a friend request for a user.

    @return: Validation of accepting the request.
'''
class ReceivedPutForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False)
    user_id = forms.CharField(required=True)
    
    def clean(self):
        cleaned_data = super(FriendsPutForm, self).clean()
        try:
            cleaned_data['user_id'] = UUID(cleaned_data['user_id'])
        except ValueError:
            raise FriendNotFoundException()
        
        if not cleaned_data['email']: del cleaned_data['email']
        
        if not cleaned_data['username']: del cleaned_data['username']
        
        if not cleaned_data['password']: del cleaned_data['password']
        
        return cleaned_data
    
    def submit(self):
        user_id = self.cleaned_data['user_id']
        del self.cleaned_data['user_id']
        
        # get the original user
        try:
            user = Friends.get(user_id)
        except CassaNotFoundException:
            raise FriendNotFoundException()
        
        if not self.cleaned_data: # no real changes made
            return FriendsSerializer(user).data
    
        # check to see username or email are being changed
        # if they are maintain the uniqueness
        if 'username' in self.cleaned_data:
            if user.username != self.cleaned_data['username'] and Friends.get(username=self.cleaned_data['username']):
                raise FriendsConflictException()
        
        if 'email' in self.cleaned_data:
            if user.email != self.cleaned_data['email'] and Friends.get(email=self.cleaned_data['email']):
                raise FriendsConflictException()
            
        if 'password' in self.cleaned_data:
            self.cleaned_data['password'] = Friends.hash_password(self.cleaned_data['password'], user.salt)
        
        user.update(self.cleaned_data)
        user.save()
        
        return FriendsSerializer(user).data

'''
    Denies a friend request for the user.

    @return: confirmation that the request was denied.
'''
class ReceivedDeleteForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = UUID(self.cleaned_data['user_id'])
            return self.cleaned_data
        except ValueError:
            raise UserNotFoundException()
    
    '''
        Submits the form to deny the friend request.
    '''
    def submit(self):
        try:
            ans = Friends.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsNotFoundException()
        except CassaNotFoundException:
            raise FriendNotFoundException()

        return FriendsSerializer(ans).data
    
        
