import pdb
from .models import Ticket
from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from ticket_capture.settings import URL_LOGIN
from .decorators import supervisor_required
from .models import Ticket
from .models import Capture
from .forms import TicketDetails, TicketCapture, Item, StoreForm

@method_decorator([login_required(login_url=URL_LOGIN), supervisor_required], name='dispatch')
class SignUp(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'


class TicketCaptureData(CreateView):
	pdb.set_trace() #debug
	models = Capture
	template_name = 'ticket_capture.html'
	form_class = TicketCapture
	second_form_class = TicketDetails
	success_url = 'ticket_capture.html'

	def get_context_data(self, **kwargs):
		context = super(TicketCaptureData, self).get_context_data(**kwargs)
		context['ticket'] = Ticket.objects.filter(confirmed = None).exclude(capture__captured_by = self.request.user.id)[0]
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if request.method == 'POST':
			form = TicketCapture(request.POST)
			if form.is_valid():
				capture = form.save()
				return HttpResponseRedirect(self.get_success_url())
			

class TicketListView(ListView):
	template_name = 'ticket_list.html'
	queryset = Ticket.objects.all()
	context_object_name = 'ticket'

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'home.html', {'form': form})

class CrearStore(CreateView):
    template_name = 'store_details.html'
    form_class = StoreForm
    success_url = reverse_lazy('TicketCaptureData')