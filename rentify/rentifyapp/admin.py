from django.contrib import admin
from .models import Car_Product , RentalRequest  

# Register your models here.
class AdminCarProduct (admin.ModelAdmin):
    list_display = (
        "userid" , 
        "carproductid",
        "car_name",
        "Luggage" , 
        "Doors",
        "Passenger",
        "description",
        "price" , 
        "image",
        'start_date',
        'end_date',
        'status',
    )

admin.site.register(Car_Product , AdminCarProduct)

class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pickup_location', 'pickup_date', 'return_location', 'return_date', 'full_name', 'email', 'phone_number')
    search_fields = ('pickup_location', 'return_location', 'full_name', 'email', 'phone_number')
    list_filter = ('pickup_date', 'return_date')

admin.site.register(RentalRequest, RentalRequestAdmin)
