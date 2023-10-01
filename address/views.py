from django.shortcuts import render
from django.conf import settings
from dotenv import load_dotenv
import os
# Create your views here.
from django.shortcuts import render
from django.views.generic.edit import CreateView

import geocoder

from .models import Address
from .forms import AddressForm



load_dotenv()    ##loads Variables in the .env file to OS.environments

MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")              


def AddressView(request):

    
    addForm = AddressForm(request.POST)
    

    if not(request.user.is_authenticated):
        # get address from the form.
        
        if (addForm.is_valid()):
            address = {}
            recieved_location = addForm.cleaned_data['address']
            g= geocoder.mapbox(recieved_location, key = MAPBOX_ACCESS_TOKEN)
            print((g.current_result))
            address['address'] = g.current_result
            
            g= g.latlng  # return g[lat][lang]
            
            address['location_lat'] = g[0]
            address['location_long'] = g[1]
            
        else:
                print("Form invalid or not filled")
                address = Address.objects.get(pk = 1)

                if (address.DoesNotExist):
                    address = {}
                    address['address'] = 'Karol Bagh'
                    address['location_lat'] = 28.652998
                    address['location_long'] = 77.189023

                
            
        
        
        context= {
            'add_form': addForm,
            'mapbox_access_token': MAPBOX_ACCESS_TOKEN,
            'addresses': address

        }
    else:
        
        if(addForm.is_valid()):

            recieved_address = addForm.cleaned_data['address']
            g= geocoder.mapbox(recieved_address, key = MAPBOX_ACCESS_TOKEN)
            recieved_address = g.current_result
            print(recieved_address)
            if Address.objects.filter(address = recieved_address).exists():
                address = Address.objects.get(address = recieved_address)
                address.users_saved.add(request.user)
            else:
                entered_address = Address.objects.create(address = recieved_address)
                entered_address.users_saved.add(request.user)

        else:
             print("Invalid Form or Not filled.")
             print(addForm)
        

        print(request.user)
        addresses = Address.objects.filter(users_saved__username = request.user )
        print(addresses)
        
        if not(addresses.count() > 0):
                print("no address for this user using Tempory")
                addresses = []
                address = {}
                address['address'] = 'Karol Bagh'
                address['location_lat'] = 28.652998
                address['location_long'] = 77.189023
                is_empty = True
                
                
                addresses.append(address)
        else:
             print("There are elements for user")
             is_empty = False

        print(addresses)
        context = {
            'add_form': addForm,
            'mapbox_access_token':MAPBOX_ACCESS_TOKEN,
            'addresses':addresses,
            'is_empty': is_empty
        }    

    return render(request , 'address/home.html' , context)
    
    