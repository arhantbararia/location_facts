from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User


from django.core.exceptions import ValidationError
from django.conf import settings
from dotenv import load_dotenv
import os



import geocoder

# Create your models here.
load_dotenv()

MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")          ##loads Variables in the .env file to OS.environments


class Address(models.Model):

    address = models.TextField()
    location_lat= models.FloatField(blank = True, null = True )
    location_long = models.FloatField(blank = True , null = True)
    users_saved = models.ManyToManyField(User , through='User_Address' , related_name= 'saved_users' )
    
    


    def save(self, *args , **kwargs ) -> None:

        if self.location_lat is None and self.location_long is None:
            g= geocoder.mapbox(self.address, key = MAPBOX_ACCESS_TOKEN)
               ## returns = [lat, long]
            
            if (g.ok == True):
                g= g.latlng
                self.location_lat = g[0]
                self.location_long = g[1]
            else:
                raise ValidationError("No results found for the location")
            

        

        return super().save(*args , **kwargs)
    



    def __str__(self):
        return self.address;




class User_Address(models.Model):
    user_id = models.ForeignKey(User , on_delete= models.CASCADE )
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)

    saved_at = models.DateTimeField(auto_now_add= True)
    
    
    class Meta:
        unique_together= ('user_id', 'address_id')


    def __str__(self) -> str:
        return f"User: {self.user_id} - Address{self.address_id}"
