# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Ticket, Store, Capture, Brand, Category, Tag, Item
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username',]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Ticket)
admin.site.register(Store)
admin.site.register(Capture)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Item)