import datetime
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Car_Product, RentalRequest
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from .forms import Step1Form, Step2Form, Step3Form, PaymentForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.serializers import serialize
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse




def search_cars(request):
    allproducts = Car_Product.objects.all()
    if request.method == 'GET':
        car_name = request.GET.get('car_name')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # Convert string dates to datetime objects
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = None

        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = None

        # Perform filtering based on the received form data
        filtered_cars = Car_Product.objects.all()
        if car_name:
            filtered_cars = filtered_cars.filter(car_name=car_name)
        if start_date and end_date:
            filtered_cars = filtered_cars.filter(start_date__lte=end_date, end_date__gte=start_date)

        context = {'filtered_cars': filtered_cars , 'allproducts' : allproducts}

        # Check if no cars are available
        if not filtered_cars.exists():
            context['no_cars_available'] = True

        return render(request, 'search_cars.html', context)


def index(req):
    username = req.user.username
    allproducts = Car_Product.objects.all()[::-1]  # Reversing the list
    context = {"username": username, "allproducts": allproducts}
    return render(req, "index.html", context)

def listing(req):
    username = req.user.username
    allproducts = Car_Product.objects.all()
    context = {"username":username , "allproducts":allproducts}
    return render(req, "listing.html" , context)

def login(req):
    if req.method == "POST":
        uname = req.POST.get("uname")
        passwd = req.POST.get("passwd")
        allproducts = Car_Product.objects.all()
        context = {}
        if not (uname and passwd):
            context['errormessage'] = "Fields can't be empty"
            return render(req, "login.html", context)
        else:
            username = uname
            userdata = authenticate(username=uname, password=passwd)
            context = {"username": username , "allproducts":allproducts}
            if userdata is not None:
                auth_login(req, userdata)
                return render(req, "index.html", context)
            else:
                context['errormessage'] = "Invalid username or password"
                return render(req, "login.html", context)
    else:
        return render(req, "login.html")

def registeruser(request):
    if request.method == "POST":
        uname = request.POST.get("uname", "")
        passwd = request.POST.get("passwd", "")
        cpasswd = request.POST.get("cpasswd", "")
        context = {}
        
        if not uname or not passwd or not cpasswd:
            context['errormessage'] = "Fields cannot be empty"
        elif passwd != cpasswd:
            context['errormessage'] = "Passwords do not match"
        else:
            try:
                # Check if user already exists
                if User.objects.filter(username=uname).exists():
                    context["errormessage"] = "User already exists"
                else:
                    # Create the user if everything is fine
                    userdata = User.objects.create_user(username=uname, password=passwd)
                    return redirect("login")
            except Exception as e:
                context["errormessage"] = "An error occurred: " + str(e)
                
        return render(request, "registeruser.html", context)
    else:
        return render(request, "registeruser.html")

def userlogout(req):
    logout(req)
    return redirect("/")

def about(req):
    username = req.user.username
    return render(req, "about.html")


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from .forms import Step1Form, Step2Form, Step3Form
from .models import RentalRequest, Car_Product  # Import Car_Product model
from django.http import HttpResponse, HttpResponseForbidden, Http404  # Import Http404
from django.urls import reverse

class RentCarWizard(SessionWizardView):
    form_list = [Step1Form, Step2Form, Step3Form]
    template_name = 'rent_form.html'

    def done(self, form_list, **kwargs):
        carproductid = self.request.session.get('carproductid')
        if carproductid:
            try:
                car_product = Car_Product.objects.get(pk=carproductid, status ='Pending')  # Ensure car is available
            except Car_Product.DoesNotExist:
                raise Http404("Car product does not exist or is not available.")  # Raise 404 if car is not available

            rental_request = RentalRequest(
                user=self.request.user,
                pickup_location=form_list[0].cleaned_data['pickup_location'],
                pickup_date=form_list[0].cleaned_data['pickup_date'],
                return_location=form_list[1].cleaned_data['return_location'],
                return_date=form_list[1].cleaned_data['return_date'],
                full_name=form_list[2].cleaned_data['full_name'],
                email=form_list[2].cleaned_data['email'],
                phone_number=form_list[2].cleaned_data['phone_number'],
                carproductid=car_product
            )
            rental_request.save()

            # Update the status of the related Car_Product
            car_product.status = 'Scheduled'
            car_product.save()

            # Add a success message
            messages.success(self.request, "Your rental request has been submitted successfully!")
            
            # Redirect to the payment page
            return redirect(reverse('checkout', kwargs={'carproductid': carproductid}))

@login_required
def rent_form(request, carproductid):
    username = request.user.username
    context = {"username":username}
    try:
        car_product = Car_Product.objects.exclude(status='Scheduled').get(pk=carproductid) 
    except Car_Product.DoesNotExist:
        return render(request, 'error_page.html', {'error_message': "The car is not available for rental."},context) 

    if request.method == 'POST':
        request.session['carproductid'] = carproductid

        form = RentCarWizard.as_view()(request)
        if isinstance(form, SessionWizardView):
            return form.done(form.get_all_cleaned_data())

    else:
        form = RentCarWizard.as_view()(request)
        
    return form


def success_page(request):
    return render(request, 'success_page.html')


def contactus(request):
    return render(request, 'contactus.html')


def Checkout(request, carproductid):

    product = Car_Product.objects.get(carproductid=carproductid)


    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': product.price,
        'item_name': product.car_name,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs = {'carproductid': product.carproductid})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'carproductid': product.carproductid})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'product': product,
        'paypal': paypal_payment
    }

    return render(request, 'checkout.html', context)

def PaymentSuccessful(request, carproductid):

    product = Car_Product.objects.get(carproductid=carproductid)


    return render(request, 'payment-success.html', {'product': product})

def paymentFailed(request, carproductid):

    product = Car_Product.objects.get(carproductid=carproductid)

    return render(request, 'payment-failed.html', {'product': product})

