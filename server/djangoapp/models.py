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
    id=1
    city="El Paso"
    state="Texas"
    st="TX"
    address="3 Nova Court"
    zip="88563"
    lat=31.6948
    long=-106.3
    short_name="Holdlamis"
    full_name="Holdlamis Car Dealership"

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    car_make= "Audi",
    car_model= "A6",
    car_year= 2010,
    dealership= 15,
    id= 1,
    name= "Berkly Shepley",
    purchase= True,
    purchase_date= "07/11/2020",
    review= "Total grid-enabled service-desk"