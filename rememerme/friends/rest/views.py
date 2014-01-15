from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rememerme.friends.serializers import FriendsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pycassa
from django.conf import settings
from rememerme.friends.rest.forms import FriendsGetListForm, FriendsPostForm, FriendsPutForm, FriendsGetSingleForm
from rememerme.friends.rest.exceptions import BadRequestException, NotImplementedException

class FriendsListView(APIView):
    '''
       Used for searching by properties or listing all friends available.
       Also, used to create new friends.
    '''
    
    def get(self, request):
        '''
            Used to search users by username or email.
        '''
        # get the offset and limit query parameters
        form = FriendsGetListForm(request.QUERY_PARAMS)
        
        if form.is_valid():
            return Response(form.submit())
        else:
            raise BadRequestException()
            

    def post(self, request):
        '''
            Used to create a new user.
        '''
        form = FriendsPostForm(request.DATA)

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
