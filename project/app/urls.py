from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('adminhome',views.adminhome,name='adminhome'),
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
    path('viewusers/', views.viewusers, name='viewusers'),
    path('view_events/', views.view_events, name='view_events'),
    path('adminview_events/', views.adminview_events, name='adminview_events'),
    path('purchase_ticket/<int:event_id>/', views.purchase_ticket, name='purchase_ticket'),
    path("payment-success/", views.payment_success, name="payment_success"),
    path('bookinghistory/', views.bookinghistory, name='bookinghistory'),
    path('bookings/', views.bookings, name='bookings'),
    path('adminbookings/', views.adminbookings, name='adminbookings'),
    path('about/', views.about, name='about'),
    path('live-score/<int:event_id>/', views.live_score, name='live_score'),
    path('event_chat/<int:event_id>/', views.event_chat, name='event_chat'),
    path('send_chat_message/<int:event_id>/', views.send_chat_message, name='send_chat_message'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('view_publishers/', views.view_publishers, name='view_publishers'),
    path('delete_publisher/<int:publisher_id>/', views.delete_publisher, name='delete_publisher'),
   
    
    

    
]
