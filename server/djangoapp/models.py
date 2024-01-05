from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
# User model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=100)
    # Create a toString method for object string representation
    def __str__(self):
        return self.name + " - " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
# Lesson
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    name = models.CharField(null=False,max_length=30)
    dealer_id = models.IntegerField()

    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    car_type = models.CharField(null=False, max_length=10, choices = CAR_TYPES, default=SEDAN)
    year = models.DateField()

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, city, st, address, zip, lat, long, short_name, full_name):
        # Dealer id
        self.id = id

        # Dealer city
        self.city = city

        # Dealer state
        self.st = st

        # Dealer address
        self.address = address

        # Dealer zip
        self.zip = zip

         # Location lat
        self.lat = lat

        # Location long
        self.long = long
        
        # Dealer short name
        self.short_name = short_name

        # Dealer Full Name
        self.full_name = full_name
        
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, id, name, dealership, review, car_make, car_model, car_year, purchase, purchase_date):
        self.car_make= car_make
        self.car_model= car_model
        self.car_year= car_year
        self.dealership= dealership
        self.id= id
        self.name= name
        self.purchase= purchase
        self.purchase_date= purchase_date
        self.review= review