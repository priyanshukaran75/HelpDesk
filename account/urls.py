from django.urls import  include,path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path("profile/edit/",views.edit,name="edit_profile"),
    path('profile/<str:username>/',views.profile_view,name='profile'),
    path("myticket/", views.myticket, name="myticket"),
    path("manage/",views.manage_tickets,name="manage_tickets"),
    path("manage/<int:id>/",views.manage_ticket_detail,name="manage_ticket_detail"),
    path("api/status/<int:ticket_id>/", views.ticket_status_api, name="ticket_status_api"),
    path("manage/update/<int:id>/",views.update_ticket_status,name="update_ticket_status"),
    path("search/",views.search_ticket,name="search_ticket"),
]