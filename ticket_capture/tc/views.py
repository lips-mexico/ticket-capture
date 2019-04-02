import pdb
from datetime import datetime
from .models import Ticket, Store
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
from .forms import *

@method_decorator([login_required(login_url=URL_LOGIN), supervisor_required], name='dispatch')
class SignUp(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'

@method_decorator([login_required(login_url=URL_LOGIN)], name='dispatch')
class TicketCaptureData(CreateView):
#	pdb.set_trace() #debug
	models = Capture
	template_name = 'ticket_capture.html'
	form_class = TicketCapture
	second_form_class = StoreForm
	success_url = reverse_lazy('item_capture')

	def get_context_data(self, **kwargs):
		context = super(TicketCaptureData, self).get_context_data(**kwargs)
		context['ticket'] = Ticket.objects.filter(confirmed = None).exclude(capture__captured_by = self.request.user.id)[0]
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context
	
	def post(self, request, *args, **kwargs):
		#pdb.set_trace() #debug
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		request_copy = request.POST.copy()
		alias = form2.data['alias']
		if alias != '':
			store = Store.objects.filter(alias = alias)
			if store:#  si la tienda existe tomo el id
				store = Store.objects.filter(alias = alias)[0]
				store_id = store.id
			else:# si la tienda no existe guardo la tienda y tomo el id generado
				store = form2.save(commit = False)
				store.rfc = 'default'
				store.save()
				store_id = store.id

			request_copy.update({'store': store_id})
			user = request.user.id
			obj = Ticket.objects.filter(confirmed = None).exclude(capture__captured_by = self.request.user.id)[0]
			ticket = obj.id
			cont = Capture.objects.filter(ticket = ticket)
			if cont:
				obj_ticket = Ticket.objects.filter(id = ticket).update(confirmed = True)
				date = form.data['ticket_date']
				time = form.data['ticket_time']
				request_copy.update({'ticket_time':date+" "+time})
				request_copy.update({'captured_by': user})
				request_copy.update({'ticket': ticket})
				form_copy = TicketCapture(request_copy)
				capture = form_copy.save()
				obj_id = capture.id
			else:
				date = form.data['ticket_date']
				time = form.data['ticket_time']
				request_copy.update({'ticket_time':date+" "+time})
				request_copy.update({'captured_by': user})
				request_copy.update({'ticket': ticket})
				form_copy = TicketCapture(request_copy)
				capture = form_copy.save()
				obj_id = capture.id

			return HttpResponseRedirect(self.get_success_url())

		else:
			user = request.user.id
			obj = Ticket.objects.filter(confirmed = None).exclude(capture__captured_by = self.request.user.id)[0]
			ticket = obj.id
			date = datetime.now()
			request_copy.update({'captured_by': user})
			request_copy.update({'ticket': ticket})
			request_copy.update({'ticket_date':date}) 
			request_copy.update({'ticket_time':date})
			request_copy.update({'branch_postal_code':'00000'}) 
			request_copy.update({'store': '8'})
			request_copy.update({'country': 'default'})
			request_copy.update({'total_amount': '0.00'})
			form_copy = TicketCapture(request_copy)
			capture = form_copy.save()

		return self.render_to_response(self.get_context_data(form=form))
		

@method_decorator([login_required(login_url=URL_LOGIN)], name='dispatch')
class ItemCapture(CreateView):
	models = Item
	form_class = ItemForm
	second_form_class = TagForm
	template_name = 'items.html'
	success_url = reverse_lazy('ticket_capture')

	def get_context_data(self, **kwargs):
		context = super(ItemCapture, self).get_context_data(**kwargs)
		context['capture'] = Capture.objects.filter(captured_by__id =self.request.user.id).last()
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		#pdb.set_trace() #debug
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		desc = form2.data['description']
		request_copy = request.POST.copy()
		if desc != '':
			tag = form2.save()
			tag_id = tag.id
			capture = Capture.objects.filter(captured_by__id =self.request.user.id).last()
			ticket = capture.id
			request_copy.update({'capture': ticket})
			request_copy.update({'tag': tag_id})
			form_copy = ItemForm(request_copy)
			form_copy.save()
			return self.render_to_response(self.get_context_data(form=form))
		else:

			return HttpResponseRedirect(self.get_success_url())


@method_decorator([login_required(login_url=URL_LOGIN)], name='dispatch')
class ControversySolving(ListView):
	template_name = 'controversy.html'
	queryset = Ticket.objects.filter(confirmed = True, valid = None).first()
	context_object_name = 'ticket'



@method_decorator([login_required(login_url=URL_LOGIN)], name='dispatch')
class TicketListView(ListView):
	template_name = 'ticket_list.html'
	queryset = Ticket.objects.all()
	context_object_name = 'ticket'
