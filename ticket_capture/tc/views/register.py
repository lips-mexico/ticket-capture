from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from ..forms import UserRegister
from ..models import User

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegister
    template_name  = 'templates/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'supervisor'
        return super().get_context_data(**kwargs)
        
    def form_valid(self, form)
        user = form.save()
        login(self.request, user)
        return redirect ('supervisor:registre_user')