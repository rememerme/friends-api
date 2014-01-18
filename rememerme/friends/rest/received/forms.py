'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for friend requests received.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin, Jake Gregg
'''
from django import forms
from rememerme.friends.models import ReceivedRequests, Friends, SentRequests
from rememerme.friends.rest.exceptions import UserNotFoundException, RequestNotFoundException
from rememerme.friends.serializers import ReceivedRequestsSerializer, FriendsSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException
import datetime

'''
    Gets all friend requests recieved and returns them to the user.

    @return: A list of requests matching the query with the given offset/limit
'''        
class ReceivedGetListForm(forms.Form):
    '''
        Submits the form and returns the friend requests received for the user.
    '''
    def submit(self, request):
        try:
            received = ReceivedRequests.getByID(request.user.pk)
        except CassaNotFoundException:
            received = {}

        return ReceivedRequestsSerializer(received).data
    
'''
    Accepts a friend request for a user.

    @return: Validation of accepting the request.
'''
class ReceivedPutForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        cleaned_data = super(ReceivedPutForm, self).clean()
        try:
            cleaned_data['user_id'] = UUID(cleaned_data['user_id'])
        except ValueError:
            raise RequestNotFoundException()
        return cleaned_data
    
    def submit(self, request):
        user_id = self.cleaned_data['user_id']
        
        # get my received requests
        try:
            received_requests = ReceivedRequests.getByID(request.user.pk)
        except CassaNotFoundException:
            received_requests = ReceivedRequests(user_id=request.user.pk)
            
        try:
            sent_requests = SentRequests.getByID(user_id)
        except CassaNotFoundException:
            sent_requests = SentRequests(user_id=request.user.pk)
        
        # check to make sure that at least one of them saw the request at some point
        # this will avoid phantom requests
        stop = not sent_requests and not received_requests
        stop2 = (sent_requests.requests and request.user.pk in sent_requests.requests)
        stop2 = stop2 or (received_requests.requests and user_id in sent_requests.requests)
        stop = stop or not stop2
            
        if stop:
            raise RequestNotFoundException()
            
        
        # the user accepted the friend request
        # so we create a friendship then delete the request
        try:
            other_friends = Friends.getByID(user_id)
        except CassaNotFoundException:
            other_friends = Friends(user_id=user_id)
        try:
            my_friends = Friends.getByID(request.user.pk)
        except CassaNotFoundException:
            my_friends = Friends(user_id=request.user.pk)
            
        now = datetime.datetime.now()
        other_friends.friends_list[request.user.pk] = now
        my_friends.friends_list[user_id] = now
        
        other_friends.save()
        my_friends.save()
        
        del received_requests.requests[user_id]
        del sent_requests.requests[request.user.pk]
        
        received_requests.save()
        sent_requests.save()
        
        return FriendsSerializer(my_friends).data
        

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
    def submit(self, request):
        user_id = self.cleaned_data['user_id']
        
        try:
            received_requests = ReceivedRequests.getByID(request.user.pk)
            del received_requests.requests[user_id]
            received_requests.save()
        except CassaNotFoundException:
            pass
            
        try:
            sent_requests = SentRequests.getByID(user_id)
            del sent_requests.requests[request.user.pk]
            sent_requests.save()
        except CassaNotFoundException:
            pass
        
        return ReceivedRequestsSerializer(received_requests).data
    
        
