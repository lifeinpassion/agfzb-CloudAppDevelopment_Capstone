from distutils.util import subst_vars
from email.policy import default
from tokenize import Name
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.timezone import now
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)
    
    def __str__(self):
        return "Make: " + self.name + "," \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
   
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CAR_TYPES = [(SEDAN, 'Sedan'),(SUV, 'SUV'), (WAGON, 'WAGON')]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False, default=0)
    model = models.CharField(null=False, max_length=30, default='model')
    name = models.CharField(null=False, max_length=30, default='dealer name')
    year = models.DateField(default=now)
    type = models.CharField(max_length=10, choices=CAR_TYPES, default=SUV)
    color = models.CharField(null=False, max_length=30, default='color')
    chassisno = models.CharField(null=False, max_length=30, default='chassis no.')

    def __str__(self):
        return self.model

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Dealership name
        self.dealership = dealership
        # Reviewer name
        self.name = name
        # Car purchase
        self.purchase = purchase
        # Review text
        self.review = review
        # Purchase date
        self.purchase_date = purchase_date
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car year
        self.car_year = car_year
        # Sentiment
        self.sentiment = sentiment
        # Review id
        self.id = id

    def __str__(self):
        return "Review: " + self.review