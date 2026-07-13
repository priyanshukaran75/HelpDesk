from django.urls import path
from . import views
app_name='ticket'
urlpatterns = [
    path('ticketcreate/', views.ticket_create, name='ticket_create'),
    path('<int:id>/', views.ticket_detail,name='ticket_detail'),
]