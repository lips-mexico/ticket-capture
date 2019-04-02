from django.urls import path
from . import views

urlpatterns = [
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('ticket_capture', views.TicketCaptureData.as_view(), name='ticket_capture'),
	path('item_capture', views.ItemCapture.as_view(), name='item_capture'),
	path('ticket_list', views.TicketListView.as_view(), name='ticket_list'),
]