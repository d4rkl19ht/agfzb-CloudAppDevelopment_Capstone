from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, dealership_add_review, get_dealer_by_state_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    # Logout user in the request
    logout(request)
    # Redirect user back to index view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        confirm_password = request.POST['confirmpassword']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        
        if password != confirm_password:
            context['username'] = username
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['password'] = password
            context['confirmpassword'] = confirm_password
            context['borderColor'] = "border border-danger"
            context['pwdDontMatch'] = "Passwords don't match"
            context['pwd_autofocus'] = "autofocus"
            return render(request, 'djangoapp/registration.html', context)
        # Check if user exists
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, state="", id=""):
    context = {}
    if request.method == "GET":
        # Get dealers from the URL
        if state:
            dealerships = get_dealer_by_state_from_cf(state)
        elif id:
            dealerships = get_dealer_by_id_from_cf(id)
        else:
            dealerships = get_dealers_from_cf()
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        json_string = json.dumps([obj.__dict__ for obj in dealerships])
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET':
        dealer_reviews = get_dealer_reviews_from_cf(dealer_id)
        context['reviews'] = dealer_reviews
        return render(request, 'djangoapp/dealer_details.html', context)
        # Concat all dealer's short name
        # dealer_reviews = ' '.join([f"{review.review} [{review.sentiment}]" for review in dealer_reviews])
        # Return a list of dealer short name
        # return HttpResponse(dealer_reviews)
    elif request.method == 'POST':
        add_review(request, dealer_id)


def add_review(request, dealer_id):
        review = {
            "id": 1114,
            "name": "Upkar Lidder 17",
            "dealership": dealer_id,
            "review": "Great service!",
            "purchase": False,
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        }
        json_payload = {}
        json_payload['review'] = review

        resp = dealership_add_review(request, review)
        # return render(request, 'djangoapp/dealer_details.html', context) 
        return HttpResponse(resp)
    