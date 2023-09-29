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
    addForm = AddressForm(request.POST or None)
    

    if not(request.user.is_authenticated):
        # get address from the form.
        
            
        if (addForm.is_valid()):
            address = {}
            address['address'] = addForm.cleaned_data['address']
            address['current_loc'] = addForm.cleaned_data['current_loc']
            g= geocoder.mapbox(address['address'], key = MAPBOX_ACCESS_TOKEN)
            
            g= g.latlng  # return g[lat][lang]
            address['location_lat'] = g[0]
            address['location_long'] = g[1]
            print(address)
        else:
                address = Address.objects.get(pk = 3)
            
        
        
        context= {
            'add_form': addForm,
            'mapbox_access_token': MAPBOX_ACCESS_TOKEN,
            'addresses': address
        }
    else:
        addresses = Address.objects.get(pk = 3)
        if(addForm.is_valid()):
            addForm.save()
        

        context = {
            'add_form': addForm,
            'mapbox_access_token':MAPBOX_ACCESS_TOKEN,
            'addresses':addresses
        }    

    return render(request , 'address/home.html' , context)
    
    