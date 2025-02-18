from django.db import models
from django.contrib.auth.models import User


class FanRegister(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    phone = models.IntegerField()
    password = models.TextField()
    location= models.TextField()
    confirm_password=models.TextField()
    favoriteevent=models.TextField()
    favoriteteam=models.TextField()

    def __str__(self):
        return self.name

class PublisherRegister(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    organization=models.TextField()
    password = models.TextField()
    location= models.TextField()
    confirm_password=models.TextField()

    def __str__(self):
        return self.name
    


class adminreg(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    phone = models.IntegerField()
    password = models.TextField()

    def __str__(self):
        return self.name
    
    
    
from django.db import models

class EventTickets(models.Model):
    publisher = models.ForeignKey(PublisherRegister, on_delete=models.CASCADE, related_name='events')  # Linking event to a publisher
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title
    
    
    


# Model to track Ticket Purchases by fans
class TicketPurchase(models.Model):
    fan = models.ForeignKey(FanRegister, on_delete=models.CASCADE)
    event = models.ForeignKey(EventTickets, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    number_of_tickets = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.fan.user.username} - {self.event.title} ({self.number_of_tickets})"
