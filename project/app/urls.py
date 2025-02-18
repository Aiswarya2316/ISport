from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('register/', views.register, name='register'),
    path('fanregister/', views.fan_register, name='fan_register'),
    path('publisherregister/', views.publisher_register, name='publisher_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('fanshome',views.fanshome,name='fanshome'),
    path('viewhome',views.viewhome,name='viewhome'),
    path('add_event/', views.add_event, name='add_event'),
    path('view_event/', views.view_event, name='view_event'),
    path('view_events/', views.view_events, name='view_events'),
    path('purchase_ticket/<int:event_id>/', views.purchase_ticket, name='purchase_ticket'),

    
]
