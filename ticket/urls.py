from django.urls import path
from . import views
app_name='ticket'
urlpatterns = [
    path('ticketcreate/', views.ticket_create, name='ticket_create'),
    path('<int:id>/', views.ticket_detail,name='ticket_detail'),
    path("delete/<int:id>/",views.delete_ticket,name="delete_ticket"),
]