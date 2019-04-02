# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
import datetime 
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'is_typist', 'is_classifier', 'is_supervisor')
        
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email',)

class TicketDetails(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [ 
          'valid', 
        ]
        labels = {'valid': "Valid", }

class TicketCapture(forms.ModelForm):
    class Meta:
        model = Capture
        fields = [
          'captured_by',
          'ticket',
          'ticket_date',
          'ticket_time',
          'branch_postal_code',
          'store',
          'country',
          'total_amount',
          'evaluated',
          'evaluated_by',
          'valid',
        ]
        labels = {
          'ticket_date': 'Ticket Date',
          'ticket_time': 'Ticket Time',
          'branch_postal_code': 'Branch Postal Code',
          'store': 'Store',
          'country': 'Contry',
          'total_amount': 'Total Amount',
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
          'unit_price', 
          'price',
          'quantity',
        ]
        labels = {
          'unit_price': 'Unit Price', 
          'price': 'Price',
          'quantity': 'Quantity',
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['description']
        labels = {'description': 'Description'}

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['alias']
        labels = {'alias': 'Store'}