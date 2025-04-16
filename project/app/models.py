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

from django.db import models

class PublisherRegister(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    email = models.EmailField(unique=True)
    name = models.TextField()
    organization = models.TextField()
    password = models.TextField()
    location = models.TextField()
    confirm_password = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Default is Pending

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
    publisher = models.ForeignKey(PublisherRegister, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # New field for ticket stock

    def __str__(self):
        return self.title

    
    


# Model to track Ticket Purchases by fans
class TicketPurchase(models.Model):
    fan = models.ForeignKey(FanRegister, on_delete=models.CASCADE)
    event = models.ForeignKey(EventTickets, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    number_of_tickets = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")], default="Pending")

    def __str__(self):
        return f"{self.fan.name} - {self.event.title} ({self.number_of_tickets})"




from django.db import models

class LiveScore(models.Model):
    event = models.OneToOneField(EventTickets, on_delete=models.CASCADE, related_name="live_score")
    team_a = models.CharField(max_length=255)
    team_b = models.CharField(max_length=255)
    score_a = models.IntegerField(default=0)
    score_b = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event.title}: {self.team_a} {self.score_a} - {self.score_b} {self.team_b}"



from django.db import models
from django.utils.timezone import now

class ChatMessage(models.Model):
    fan = models.ForeignKey(FanRegister, on_delete=models.CASCADE)
    publisher = models.ForeignKey(PublisherRegister, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.fan.name} -> {self.publisher.name}: {self.message[:30]}"




from django.db import models

class AdminNotification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
