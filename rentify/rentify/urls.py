from django.contrib import admin
from django.urls import path, include
from rentifyapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("rentifyapp.urls")),
    path('login/', views.login, name="login"), 
     path('/', views.index, name="index"),
    path('registeruser/', views.registeruser, name="registeruser"),
    path('userlogout/', views.userlogout, name="userlogout"),
    path('search_cars/', views.search_cars, name="search_cars"),
    path('about/', views.about, name="about"),
    path('listing/', views.listing, name="listing"),
    path("accounts/", include("allauth.urls")),
    path('rent_form/<int:carproductid>/', views.rent_form, name='rent_form'),
    path('checkout/<int:carproductid>/', views.Checkout, name='checkout'),
    path('payment-success/<int:carproductid>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:carproductid>/', views.paymentFailed, name='payment-failed'),
    path('contactus/', views.contactus, name='contactus'),
    path('social-auth/',include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

