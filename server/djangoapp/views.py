from operator import truediv
from os import name
from symbol import yield_arg
from time import strptime
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import CarDealer, CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, get_dealers_by_st_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json




# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, 'djangoapp/static.html')

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'Invalid username or password.'
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/10657071-dcad-4804-b442-82c3946a252e/dealership-package/dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return render(request, 'djangoapp/index.html', context)
        #return HttpResponse(dealer_names)
        context = {}
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    context = {}
    if request.method == "GET":
        #dealer details
        dealer = get_dealer_by_id_from_cf("https://au-syd.functions.appdomain.cloud/api/v1/web/10657071-dcad-4804-b442-82c3946a252e/dealership-package/dealership.json", id=id)
        context["dealer"] = dealer
        # dealer reviews
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/10657071-dcad-4804-b442-82c3946a252e/dealership-package/get-review.json"
        reviews = get_dealer_reviews_from_cf(url, id=id)
        context["review_list"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            context= {}
            cars = CarModel.objects.filter(dealer_id=dealer_id)
            context['cars'] = cars
            # get dealer information
            context['dealer'] = get_dealer_by_id_from_cf(
                'https://au-syd.functions.appdomain.cloud/api/v1/web/10657071-dcad-4804-b442-82c3946a252e/dealership-package/dealership.json', id=dealer_id
            )
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == 'POST':
            # deal with the purchasecheck field
            purchase = request.POST.get('purchasecheck')
            if purchase is None:
                purchase = False
            else:
                if purchase == 'on':
                    purchase = True
                else:
                    purchase = False

            review = {
                'time': datetime.utcnow().isoformat(),
                'dealership': dealer_id,
                'review': request.POST['content'],
                'name': ' '.join([request.user.first_name, request.user.last_name]),
                'purchase': purchase
            }

            if review['purchase']:
                car = CarModel.objects.get(id=int(request.POST['car']))
                review.update({
                    'car_make': car.car_make.name,
                    'car_model': car.name,
                    'car_year': car.year.year,
                    'purchase_date': request.POST['purchasedate']
                })
            json_payload = {
                'review': review,            
            }
            response = post_request('https://au-syd.functions.appdomain.cloud/api/v1/web/10657071-dcad-4804-b442-82c3946a252e/dealership-package/post-review', 
                                    json_payload, dealer_id=dealer_id)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)