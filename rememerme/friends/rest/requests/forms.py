'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for friend requests.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin, Jake Gregg
'''
from django import forms
from config.util import getLimit
import bcrypt
from rememerme.friends.models import Requests
from config import util
from rememerme.friends.rest.requests.exceptions import UserNotFoundException, RequestsListNotFoundException, AlreadyFriendsException, RequestAlreadySentException
from rememerme.friends.serializers import RequestsSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException
'''
    Creates a friend request.
'''
class RequestsPostForm(forms.Form):
    user_id = forms.CharField(required=True)
    friend_id = forms.CharField(required=True)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        try:
            self.cleaned_data['user_id'] = uuid.UUID(self.cleaned_data['user_id'])
            self.cleaned_data['friend_id'] = uuid.UUID(self.cleaned_data['friend_id'])
            return self.cleaned_data
        except ValueError:
            raise UserNotFoundException()
        return self.cleaned_data
    
    '''
        Submits the form and makes a friend request sent for the user and a 
        friend request received for the other user.
    '''
    def submit(self):
        user_friends = Friends.getByID(self.cleaned_data['user_id'])
        # If they are already friends, don't add them again. 
        # Raise the error.
        if self.cleaned_data['friend_id'] in user_friends.friend_list:
            raise AlreadyFriendsException()
        # If they have arleady sent a request, don't add another one.
        # Raise an error.
        user_request = Requests.getByID(self.cleaned_data['user_id'])
        if self.cleaned_data['friend_id'] in user_request.sent:
            raise RequestAlreadySentException()
        user_request.sent[self.cleaned_data['friend_id']] = self.cleaned_data['friend_id']

        other_friends = Friends.getByID(self.cleaned_data['friend_id'])
        # If they are already friends, don't add them again. 
        # Raise the error.
        if self.cleaned_data['user_id'] in other_friends.friend_list:
            raise AlreadyFriendsException()

        other_request = Requests.getByID(self.cleaned_data['friend_id'])
        # If they have arleady received a request, don't add another one.
        # Raise an error.
        if self.cleaned_data['user_id'] in other_request.received:
            raise RequestAlreadySentException()
        other_request.received[self.cleaned_data['user_id']] = self.cleaned_data['user_id']

        user_request.save()
        other_request.save()
        return RequestsSerializer(user).data
'''
    Gets a list of all requests made by a user.
        
    @return: A list of requests matching the query with the given offset/limit
'''        
class RequestsGetForm(forms.Form):
    user_id = forms.CharField(required=False)

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
        Submits the form and gets the requests for a given user.
        
        @return: A list of users matching the query with the given offset/limit
    '''
    def submit(self):
        try:
            ans = Requests.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise RequestsListNotFoundException()
        except CassaNotFoundException:
            raise RequestsListNotFoundException()

        return RequestsSerializer(ans).data


