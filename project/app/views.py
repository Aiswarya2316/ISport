from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def get_admin(request):
    """Retrieve the logged-in staff object from the session."""
    if 'admin' not in request.session:
        return None  
    try:
        return PublisherRegister.objects.get(email=request.session['admin'])
    except adminreg.DoesNotExist:
        return None

def get_publisher(request):
    """Retrieve the logged-in staff object from the session."""
    if 'publisher' not in request.session:
        return None  
    try:
        return PublisherRegister.objects.get(email=request.session['publisher'])
    except PublisherRegister.DoesNotExist:
        return None
    
def get_fans(request):
    """Retrieve the logged-in staff object from the session."""
    if 'fans' not in request.session:
        return None  
    try:
        return FanRegister.objects.get(email=request.session['fans'])
    except FanRegister.DoesNotExist:
        return None


import re

def fan_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('fan_register')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Invalid email format!")
            return redirect('fan_register')

        # ✅ Phone number validation (10-digit example)
        if not re.match(r"^\d{10}$", phone):
            messages.error(request, "Invalid phone number! Enter a 10-digit number.")
            return redirect('fan_register')

        if FanRegister.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('fan_register')

        donor = FanRegister(
            name=name,
            email=email,
            phone=phone,
            location=location,
            password=password,
            confirm_password=confirm_password
        )
        donor.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'bookers/fan_register.html')



from .models import AdminNotification

def publisher_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        location = request.POST['location']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('publisher_register')
        
        if PublisherRegister.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('publisher_register')

        staff = PublisherRegister(name=name, email=email, location=location, password=password)
        staff.save()

        # Create admin notification
        AdminNotification.objects.create(message=f"New publisher registered: {staff.name}")

        messages.success(request, "Publisher registered successfully!")
        return redirect('login')

    return render(request, 'publisher/publisher_register.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        password = request.POST['password']       
        if adminreg.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken!")
            return redirect('register')
        admin = adminreg(email=email, name=name, phone=phone, password=password)
        admin.save()
        user = User.objects.create_user(username=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        messages.success(request, "Admin registered successfully!")
        return redirect('admin_login')
    return render(request, 'admin/admin_register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            donor = FanRegister.objects.get(email=email, password=password)
            request.session['fan'] = donor.email
            return redirect('fanshome')  
        except FanRegister.DoesNotExist:
            pass  
        try:
            staff = PublisherRegister.objects.get(email=email, password=password)
            request.session['publisher'] = staff.id  # Store ID instead of email
            return redirect('viewhome')  
        except PublisherRegister.DoesNotExist:
            pass  
        messages.error(request, "Invalid login credentials!")
        return redirect('login')  
    return render(request, 'login.html')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        try:
            admin = adminreg.objects.get(email=email , password=password)
            request.session['admin'] = admin.email
            return redirect('adminhome')             
        except adminreg.DoesNotExist:
            messages.error(request, "No admin account found with this email!")
            return redirect('admin_login')
    return render(request, 'admin/adminlogin.html')



def user_logout(request):
    if 'fans' in request.session:
        del request.session['fans']
    if 'publisher' in request.session:
        del request.session['publisher']
    if 'admin' in request.session:
        del request.session['admin']
        logout(request)

    return redirect('home')




def home(request):
    return render(request,'home.html')



def fanshome(request):
    return render(request,'bookers/fanshome.html')



def viewhome(request):
    return render(request,'publisher/viewhome.html')



from .models import AdminNotification

def adminhome(request):
    notifications = AdminNotification.objects.filter(is_read=False).order_by('-timestamp')
    return render(request, 'admin/admin_home.html', {'notifications': notifications})













# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PublisherRegister, EventTickets, FanRegister, TicketPurchase
from django.core.exceptions import ObjectDoesNotExist





from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime

def add_event(request):
    if request.method == 'POST':
        publisher_name = request.POST.get('publisher_name')

        try:
            publisher = PublisherRegister.objects.get(name=publisher_name)
        except ObjectDoesNotExist:
            return HttpResponse("Publisher with this name does not exist.", status=404)

        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        # Parse and validate the date
        try:
            date = parse_date(date_str)
            if date < datetime.date.today():
                return HttpResponse("Event date cannot be in the past.", status=400)
        except:
            return HttpResponse("Invalid date format.", status=400)

        if title and description and date and location and price and stock:
            event = EventTickets.objects.create(
                publisher=publisher,
                title=title,
                description=description,
                date=date,
                location=location,
                price=price,
                stock=int(stock)
            )
            return redirect('view_event')

        else:
            return HttpResponse("Please fill in all the fields", status=400)

    return render(request, 'publisher/add_event.html')




def view_event(request):
    events = EventTickets.objects.all()
    return render(request, 'publisher/view_events.html', {'events': events})




from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import EventTickets

def delete_event(request, event_id):
    publisher_id = request.session.get('publisher')  # Get the logged-in publisher ID

    event = get_object_or_404(EventTickets, id=event_id)  # Get the event

    if event.publisher_id != publisher_id:  # Check if the event belongs to the logged-in publisher
        messages.error(request, "You are not authorized to delete this event!")  
        return redirect('view_event')  # Redirect without deleting

    event.delete()  # Delete only if the publisher matches
    messages.success(request, "Event deleted successfully!")
    return redirect('view_event')






# View for displaying all events
from django.db.models import Q
from .models import EventTickets

def view_events(request):
    query = request.GET.get('location')
    if query:
        events = EventTickets.objects.filter(location__icontains=query)
    else:
        events = EventTickets.objects.all()
    return render(request, 'bookers/view_events.html', {'events': events, 'search_query': query})



def adminview_events(request):
    events = EventTickets.objects.all()
    return render(request, 'admin/view_events.html', {'events': events})







import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import TicketPurchase, EventTickets, FanRegister
from datetime import date

def purchase_ticket(request, event_id):
    event = get_object_or_404(EventTickets, id=event_id)

    # Prevent booking for past events
    if event.date < date.today():
        return render(request, "bookers/purchase_ticket.html", {
            "event": event,
            "error": "You cannot book tickets for past events."
        })

    if request.method == "POST":
        fan_name = request.POST["fan_name"]
        num_tickets = int(request.POST["number_of_tickets"])

        # ✅ Stock check
        if num_tickets > event.stock:
            return render(request, "bookers/purchase_ticket.html", {
                "event": event,
                "error": f"Only {event.stock} tickets are available."
            })

        total_amount = event.price * num_tickets * 100  # Convert to paise

        if total_amount > 50000000:
            return render(request, "bookers/purchase_ticket.html", {
                "event": event,
                "error": "Total amount exceeds the allowed limit of ₹5,00,000 per transaction."
            })

        fan = FanRegister.objects.filter(name=fan_name).first()

        if not fan:
            return render(request, "bookers/purchase_ticket.html", {
                "event": event,
                "error": "Fan not registered."
            })

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order_data = {
            "amount": int(total_amount),
            "currency": "INR",
            "payment_capture": "1"
        }
        order = client.order.create(order_data)

        ticket_purchase = TicketPurchase.objects.create(
            fan=fan,
            event=event,
            number_of_tickets=num_tickets,
            amount=total_amount / 100,
            razorpay_order_id=order["id"]
        )

        context = {
            "event": event,
            "order_id": order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": total_amount,
            "fan_name": fan.name
        }

        return render(request, "bookers/payment.html", context)

    return render(request, "bookers/purchase_ticket.html", {"event": event})


@csrf_exempt
def payment_success(request):
    order_id = request.GET.get("order_id")
    ticket_purchase = TicketPurchase.objects.filter(razorpay_order_id=order_id).first()

    if ticket_purchase and ticket_purchase.payment_status != "Paid":
        ticket_purchase.payment_status = "Paid"
        ticket_purchase.save()

        # Decrease stock
        event = ticket_purchase.event
        event.stock -= ticket_purchase.number_of_tickets
        event.save()

    return render(request, "bookers/success.html", {"ticket": ticket_purchase})





from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TicketPurchase, FanRegister

def bookinghistory(request):
    if 'fan' in request.session:  # Check if a fan is logged in
        fan_email = request.session['fan']
        try:
            fan = FanRegister.objects.get(email=fan_email)
            bookings = TicketPurchase.objects.filter(fan=fan)  # Fetch only the logged-in fan's bookings
            return render(request, 'bookers/bookinghistory.html', {'bookings': bookings})
        except FanRegister.DoesNotExist:
            messages.error(request, "User not found!")
            return redirect('login')
    else:
        messages.error(request, "Please log in to view your booking history!")
        return redirect('login')

def cancel_booking(request, booking_id):
    if 'fan' in request.session:  # Check if a fan is logged in
        fan_email = request.session['fan']
        try:
            fan = FanRegister.objects.get(email=fan_email)
            booking = TicketPurchase.objects.get(id=booking_id, fan=fan)  # Ensure the user owns this booking
            booking.delete()
            messages.success(request, "Booking cancelled successfully!")
        except TicketPurchase.DoesNotExist:
            messages.error(request, "Booking not found or unauthorized!")
    return redirect('bookinghistory')



def bookings(request):
    events = TicketPurchase.objects.all()
    return render(request,'publisher/bookings.html',{'events':events})


def adminbookings(request):
    events = TicketPurchase.objects.all()
    return render(request,'admin/bookings.html',{'events':events})






def viewusers(request):
    users=FanRegister.objects.all()
    return render(request,'admin/viewusers.html',{'users':users})



def about(request):
    return render(request,'bookers/aboutus.html')



from django.http import JsonResponse
from .models import LiveScore

def live_score(request, event_id):
    try:
        score = LiveScore.objects.get(event_id=event_id)
        data = {
            "event": score.event.title,
            "team_a": score.team_a,
            "team_b": score.team_b,
            "score_a": score.score_a,
            "score_b": score.score_b,
            "last_updated": score.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        }
    except LiveScore.DoesNotExist:
        # Set default values when no live score is available
        data = {
            "event": "Unknown Event",
            "team_a": "Team A",
            "team_b": "Team B",
            "score_a": 0,
            "score_b": 0,
            "last_updated": "N/A"
        }
    
    return JsonResponse(data)




from django.shortcuts import render, get_object_or_404
from .models import EventTickets, ChatMessage

def event_chat(request, event_id):
    event = get_object_or_404(EventTickets, id=event_id)

    # Simulating a live score fetch - replace this with an actual API call if available
    live_score = {
        "team_a": "Team A",
        "team_b": "Team B",
        "score_a": 1,
        "score_b": 2
    }

    # Fetch all messages for this event
    chat_messages = ChatMessage.objects.filter(publisher=event.publisher).order_by('timestamp')

    return render(request, 'bookers/chat.html', {
        'event': event,
        'live_score': live_score,
        'chat_messages': chat_messages
    })







from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import ChatMessage, FanRegister, EventTickets

def send_chat_message(request, event_id):
    if request.method == "POST":
        message_text = request.POST.get("message")
        fan_name = request.POST.get("name")  # Get fan name from form input
        event = get_object_or_404(EventTickets, id=event_id)

        # Create or retrieve the fan by name (no authentication required)
        fan, created = FanRegister.objects.get_or_create(name=fan_name)

        # Store the message
        ChatMessage.objects.create(
            fan=fan,
            publisher=event.publisher,
            message=message_text
        )

    return HttpResponseRedirect(reverse('event_chat', args=[event_id]))






from django.shortcuts import render, redirect
from .models import PublisherRegister

def view_publishers(request):
    if 'admin' not in request.session:
        return redirect('login')  # Ensure only admin can access
    publishers = PublisherRegister.objects.all()
    return render(request, 'admin/view_publishers.html', {'publishers': publishers})


from django.shortcuts import render, redirect, get_object_or_404
from .models import PublisherRegister
from django.contrib import messages

def delete_publisher(request, publisher_id):
    if 'admin' not in request.session:
        return redirect('admin_login')  # Ensure only admin can access
    
    # Retrieve and delete publisher
    publisher = get_object_or_404(PublisherRegister, id=publisher_id)
    publisher.delete()
    messages.success(request, "Publisher deleted successfully.")
    return redirect('view_publishers')



from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .models import PublisherRegister

def manage_publisher(request):
    if not request.session.get('admin'):  # Check if the admin is logged in
        messages.error(request, "You are not authorized to access this page.")
        return redirect('admin_login')

    publishers = PublisherRegister.objects.filter(status='pending')  # Show only pending approvals
    return render(request, 'admin/manage_publisher.html', {'publishers': publishers})

def approve_publisher(request, publisher_id):
    publisher = get_object_or_404(PublisherRegister, id=publisher_id)
    publisher.status = 'approved'
    publisher.save()
    messages.success(request, f"{publisher.name} has been approved!")
    return redirect('manage_publisher')

def reject_publisher(request, publisher_id):
    publisher = get_object_or_404(PublisherRegister, id=publisher_id)
    publisher.status = 'rejected'
    publisher.save()
    messages.warning(request, f"{publisher.name} has been rejected!")
    return redirect('manage_publisher')

