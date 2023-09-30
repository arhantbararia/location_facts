from django import forms
from .models import Address

def get_current_user(request):
    return request.user

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["address"]