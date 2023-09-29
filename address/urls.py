from django.contrib import admin
from django.urls import path, include
from .views import AddressView

urlpatterns = [
    path('nice/' , AddressView , name = 'location_facts'),
    
]
