from django.shortcuts import render, redirect , get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import userModel
from .models import photos
from .models import faqsQA
from .models import testimonial
from .models import eventPage
from .models import quiry
from .models import Package
from .models import Booking
from .forms import userForm
from .forms import quiryForm
import json

import io
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render
from .models import Booking
from datetime import datetime, timedelta
#from xhtml2pdf import pisa  # Install using `pip install xhtml2pdf`
from .models import Booking


#Create Your Views Here

# Create your views here.
def registration(request):
    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            contact = form.cleaned_data['contact']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            cpassword = form.cleaned_data['cpassword']

            if password == cpassword:  # Check if passwords match
                data = userModel(username=username, contact=contact, email=email, password=password , cpassword=cpassword)
                data.save()
                return redirect('Login_Page.html')  # Redirect to the login page (URL name, not HTML file)
            else:
                return render(request, 'app/regi.html', {'form': form, 'error_message': 'Confirm Passwords do not match.'})
        else:
            return render(request, 'app/regi.html', {'form': form})
    else:
        form = userForm()
    return render(request, 'app/regi.html', {'form': form})


def Home(request):
    products = testimonial.get_all_products()
    return render(request,"app/Home_Page.html", {'testimonial':products})

def about_us(request):
    return render(request, 'app/About_Us.html')

def contactUs(request):
    if request.method == 'POST':
        form = quiryForm(request.POST)
        if form.is_valid():
           uname = form.cleaned_data['uname']
           umail = form.cleaned_data['umail']
           uquery = form.cleaned_data['uquery']

           data = quiry(uname=uname,umail=umail,uquery=uquery)
           data.save()
    else:
        form = quiryForm()
    return render(request, 'app/Contact_Us.html')

def Event(request):
    products = eventPage.get_all_products()
    return render(request,"app/Event.html", {'eventPage':products})

def faqs(request):
    products = faqsQA.get_all_products()
    return render(request,"app/FAQs_Page.html", {'faqsQA':products})

def gallary(request):
    products = photos.get_all_products()
    return render(request,"app/Gallary_Page.html", {'photos':products})

def login(request):
    if request.method == 'GET':
        return render(request, 'app/Login_Page.html')
    else:
        username1 = request.POST.get('username1')
        password1 = request.POST.get('password1')
        try:
            customer = userModel.objects.get(email=username1, password=password1)
            # Storing user details in the session
            request.session['user_id'] = customer.id
            request.session['username'] = customer.username  # Store the username
            return redirect('Home')
        except userModel.DoesNotExist:
            error_message = "Invalid username or password!!"
            return render(request, 'app/Login_Page.html', {'error_message': error_message})

@require_POST
def logout_view(request):
    request.session.flush()
    return redirect('Home')

def package(request,event_id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        # If the user is not logged in, return a forbidden response or redirect to login
         return render(request, 'app/Login_Page.html')  # You can also use `HttpResponseForbidden('You are not authorized to view this page.')`
    
    event = get_object_or_404(eventPage, pk=event_id)
    packages = Package.objects.filter(event=event)
    return render(request, 'app/EV_CA.html', {'event': event, 'packages': packages})

@csrf_exempt
def confirm_booking(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'success': False, 'error': 'User not authenticated.'})

            user = userModel.objects.get(id=user_id)

            # Retrieve form data
            address = request.POST.get('address')
            event_date = request.POST.get('event_date')
            event_time = request.POST.get('event_time')
            cart_data = request.POST.get('cart')
            subtotal = request.POST.get('subtotal')

            if not cart_data:
                return JsonResponse({'success': False, 'error': 'No cart data received.'})

            cart_items = json.loads(cart_data)

            for item in cart_items:
                package = Package.objects.get(id=item['id'])
                Booking.objects.create(
                    user=user,
                    package=package,
                    package_name=item['name'],
                    price=item['price'],
                    address=address,
                    event_date=event_date,
                    event_time=event_time,
                )

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        

def generate_report(request, report_type):
    # Determine the date range
    if report_type == "weekly":
        start_date = datetime.now() - timedelta(days=7)
    elif report_type == "monthly":
        start_date = datetime.now() - timedelta(days=30)
    elif report_type == "yearly":
        start_date = datetime.now() - timedelta(days=365)
    else:
        return HttpResponse("Invalid report type", status=400)

    # Fetch relevant bookings
    bookings = Booking.objects.filter(event_date__gte=start_date)

    # Load template
    template = get_template("app/report_template.html")
    context = {"bookings": bookings, "report_type": report_type}
    html = template.render(context)

    # Generate PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{report_type}_report.pdf"'
    
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), response)
    
    if pdf.err:
        return HttpResponse("Error generating PDF", status=500)

    return response