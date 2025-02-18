# admin.py

from django.contrib import admin
from .models import FanRegister, PublisherRegister, EventTickets, TicketPurchase

admin.site.register(FanRegister)
admin.site.register(PublisherRegister)
admin.site.register(EventTickets)
admin.site.register(TicketPurchase)
