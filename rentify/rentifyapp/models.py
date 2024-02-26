import datetime
from django.db import models
from django.contrib.auth.models import User

class CustomManager(models.Manager):
    def search_by_type(self, car_type):
        return self.filter(car_name=car_type)

    def search_all(self):
        return self.all()


class Car_Product(models.Model):
    userid = models.ForeignKey(User , on_delete = models.CASCADE , null = True , blank = True)
    carproductid = models.IntegerField(primary_key = True)
    car_name = models.CharField(max_length = 55)
    Luggage = models.IntegerField()
    Doors =models.IntegerField()
    Passenger = models.IntegerField()
    description = models.TextField(max_length = 100)
    price = models.FloatField()
    image=models.ImageField(upload_to='car_product/')
    objects = models.Manager()
    prod = CustomManager()
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)

    OPTION_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Approved', 'Approved'),
        ('On Hold', 'On Hold'),
        ('Rejected', 'Rejected'),
        ('Scheduled', 'Scheduled')
    )
    status = models.CharField(max_length=20, choices=OPTION_CHOICES, default='Pending')

class RentalRequest(models.Model):
    carproductid = models.ForeignKey(Car_Product , on_delete = models.CASCADE , null = True , blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=100)
    pickup_date = models.DateField()
    return_location = models.CharField(max_length=100)
    return_date = models.DateField()
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

