'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for users.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin
'''
from django import forms
from config.util import getLimit
import bcrypt
from rememerme.friends.models import Friends
from config import util
from rememerme.friends.rest.friends.exceptions import FriendConflictException, FriendNotFoundException
from rememerme.friends.serializers import FriendsSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

class FriendsPostForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    facebook = forms.BooleanField(required=False)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        self.cleaned_data['premium'] = False
        self.cleaned_data['active'] = True
        self.cleaned_data['facebook'] = self.cleaned_data['facebook'] if 'facebook' in self.cleaned_data else False
        self.cleaned_data['salt'] = bcrypt.gensalt()
        self.cleaned_data['password'] = Friends.hash_password(self.cleaned_data['password'], self.cleaned_data['salt'])
        return self.cleaned_data
    
    '''
        Submits this form to retrieve the correct information requested by the user.
        Defaults to search by username. Then, will check if the email parameter is
        provided.
        
        This means a query with email and username both set will ignore username.
        
        @return: A list of users matching the query with the given offset/limit
    '''
    def submit(self):
        user = Friends.fromMap(self.cleaned_data)
        # check if username and email have not been used yet
        # if they have not then save the user
        if Friends.getByEmail(user.email) or Friends.getByUsername(user.username):
            raise FriendConflictException()
        
        user.save()
        return FriendsSerializer(user).data
'''
    Submits this form and returns the friends of the currrent user.
        
    This means a query with email and username both set will ignore username.
        
    @return: A list of users matching the query with the given offset/limit
'''        
class FriendsGetListForm(forms.Form):
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
        Submits this form to retrieve the correct information requested by the user.
        Defaults to search by username. Then, will check if the email parameter is
        provided.
        
        This means a query with email and username both set will ignore username.
        
        @return: A list of users matching the query with the given offset/limit
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
            ans = Friends.getByID(self.cleaned_data['user_id'])
            if not ans:
                raise FriendsNotFoundException()
        except CassaNotFoundException:
            raise FriendNotFoundException()

        return FriendsSerializer(ans).data
    
class FriendsPutForm(forms.Form):
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
    

    
        
