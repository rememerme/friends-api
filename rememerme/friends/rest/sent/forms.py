'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for friend requests received.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin, Jake Gregg
'''
from django import forms
from rememerme.friends.models import ReceivedRequests, SentRequests
from rememerme.friends.rest.exceptions import UserNotFoundException
from rememerme.friends.serializers import SentRequestsSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException

'''
    Gets all friend requests recieved and returns them to the user.

    @return: A list of requests matching the query with the given offset/limit
'''        
class SentGetListForm(forms.Form):
    '''
        Submits the form and returns the friend requests received for the user.
    '''
    def submit(self, request):
        try:
            sent = SentRequests.getByID(request.user.pk)
        except CassaNotFoundException:
            sent = SentRequests(user_id=request.user.pk, requests={})

        return SentRequestsSerializer(sent).data
        

'''
    Denies a friend request for the user.

    @return: confirmation that the request was denied.
'''
class SentDeleteForm(forms.Form):
    user_id = forms.CharField(required=True)
    
    def clean(self):
        try:
            self.cleaned_data['user_id'] = str(UUID(self.cleaned_data['user_id']))
            return self.cleaned_data
        except ValueError:
            raise UserNotFoundException()
    
    '''
        Submits the form to deny the friend request.
    '''
    def submit(self, request):
        user_id = self.cleaned_data['user_id']
        
        try:
            received_requests = ReceivedRequests.getByID(user_id)
            del received_requests.requests[request.user.pk]
            received_requests.save()
        except CassaNotFoundException:
            pass
            
        try:
            sent_requests = SentRequests.getByID(request.user.pk)
            del sent_requests.requests[user_id]
            sent_requests.save()
        except CassaNotFoundException:
            sent_requests = SentRequests(user_id=request.user.pk)

        return SentRequestsSerializer(sent_requests).data
    
        
