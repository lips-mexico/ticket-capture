from django.urls import path
from . import views

urlpatterns = [
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('ticket_capture', views.TicketCaptureData.as_view(), name='ticket_capture'),
	path('create_store', views.CrearStore.as_view(), name="create_store"),
	path('ticket_details', views.get_name, name='ticket_details'),
	path('ticket_list', views.TicketListView.as_view(), name='ticket_list'),
]