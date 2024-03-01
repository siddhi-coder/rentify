from django.urls import path,include
from . import views

urlpatterns = [
    path("" , views.index),
    path("logout", views.userlogout),
    path('rent_form/<int:carproductid>/', views.rent_form, name='rent_form'),
    path('', include('paypal.standard.ipn.urls')),
    ]