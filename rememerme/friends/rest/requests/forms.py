'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for friend requests.
    
    Created on Dec 20, 2013

    @author: Andrew Oberlin, Jake Gregg
'''
from django import forms
from rememerme.friends.models import ReceivedRequests, SentRequests
from rememerme.friends.rest.exceptions import UserNotFoundException
from rememerme.friends.serializers import SentRequestsSerializer
from uuid import UUID
from pycassa.cassandra.ttypes import NotFoundException as CassaNotFoundException
import datetime

'''
    Creates a friend request.
'''
class RequestsPostForm(forms.Form):
    user_id = forms.CharField(required=True)

    '''
        Overriding the clean method to add the default offset and limiting information.
    '''
    def clean(self):
        try:
            UUID(self.cleaned_data['user_id'])
        except ValueError:
            raise UserNotFoundException()
        return self.cleaned_data
    
    '''
        Submits the form and makes a friend request sent for the user and a 
        friend request received for the other user.
    '''
    def submit(self, request):
        user_id = self.cleaned_data['user_id']
        try:
            received = ReceivedRequests.getByID(user_id)
        except CassaNotFoundException:
            received = ReceivedRequests(user_id=user_id, requests={})
            
        now = datetime.datetime.now().isoformat()
        received.requests[request.user.pk] = now
        received.save()
        
        try:
            sent = SentRequests.getByID(request.user.pk)
        except CassaNotFoundException:
            sent = SentRequests(user_id=request.user.pk, requests={})
        
        sent.requests[user_id] = now
        sent.save()
        
        return SentRequestsSerializer(sent).data
        
        


