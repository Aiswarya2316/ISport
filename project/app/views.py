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
        if FanRegister.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('fan_register')
        donor = FanRegister(name=name, email=email, phone=phone, location=location, password=password , confirm_password=confirm_password)
        donor.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')
    return render(request, 'bookers/fan_register.html')


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
        staff = PublisherRegister(name=name, email=email,  location=location, password=password ,confirm_password=confirm_password)
        staff.save()
        messages.success(request, "publisher registered successfully!")
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
            request.session['publisher'] = staff.email
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



def adminhome(request):
    return render(request,'admin/admin_home.html')










# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PublisherRegister, EventTickets, FanRegister, TicketPurchase
from django.core.exceptions import ObjectDoesNotExist


# Publisher adds event ticket details
def add_event(request):
    if request.method == 'POST':
        publisher_name = request.POST.get('publisher_name')

        try:
            # Try to find the publisher by name
            publisher = PublisherRegister.objects.get(name=publisher_name)

        except ObjectDoesNotExist:
            # If no publisher found, return an error message
            return HttpResponse("Publisher with this name does not exist.", status=404)

        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')
        price = request.POST.get('price')

        if title and description and date and location and price:
            event = EventTickets.objects.create(
                publisher=publisher,
                title=title,
                description=description,
                date=date,
                location=location,
                price=price
            )
            return redirect('view_event')  # Redirect to events page after adding

        else:
            return HttpResponse("Please fill in all the fields", status=400)

    return render(request, 'publisher/add_event.html')




def view_event(request):
    events = EventTickets.objects.all()
    return render(request, 'publisher/view_events.html', {'events': events})


# View for displaying all events
def view_events(request):
    events = EventTickets.objects.all()
    return render(request, 'bookers/view_events.html', {'events': events})




def adminview_events(request):
    events = EventTickets.objects.all()
    return render(request, 'admin/view_events.html', {'events': events})








# Fan can purchase a ticket for an event
def purchase_ticket(request, event_id):
    event = EventTickets.objects.get(id=event_id)

    if request.method == 'POST':
        fan_name = request.POST.get('fan_name')
        fan = FanRegister.objects.get(name=fan_name)

        number_of_tickets = int(request.POST.get('number_of_tickets'))

        # Create a TicketPurchase object to track the purchase
        TicketPurchase.objects.create(
            fan=fan,
            event=event,
            number_of_tickets=number_of_tickets
        )

        return redirect('view_events')  # Redirect back to events page after purchase

    return render(request, 'bookers/purchase_ticket.html', {'event': event})



def bookinghistory(request):
    events = TicketPurchase.objects.all()
    return render(request,'bookers/bookinghistory.html',{'events':events})



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





