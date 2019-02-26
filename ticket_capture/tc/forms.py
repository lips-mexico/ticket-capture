# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
import datetime 
from .models import Ticket,Capture,Item,Store


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
          'ticket',
          'ticket_date',
          'ticket_time',
          'branch_postal_code',
          'store',
          'country',
          'total_amount',
        ]
        labels = {
          'ticket': 'Ticket',
          'ticket_date': 'Ticket Date',
          'ticket_time': 'Ticket Time',
          'branch_postal_code': 'Branch Postal Code',
          'store': 'Store',
          'country': 'Contry',
          'total_amount': 'Total Amount',
        }

class Item(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
          'capture',
          'tag',
          'unit_price', 
          'price',
          'quantity',
        ]
        labels = {
          'capture': 'Capture',
          'tag': 'Tag',
          'unit_price': 'Unit Price', 
          'price': 'Price',
          'quantity': 'Quantity',
        }

class StoreForm(forms.ModelForm):

      class Meta:
        model = Store
        fields = ['rfc','alias']

      def __init__(self, *args, **kwargs):
        super(StoreForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
          if field == 'alias':
            self.fields[field].widget.atrs.update({
                'class': 'form-control'
                 })
