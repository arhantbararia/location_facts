from django.contrib import admin
from .models import Address, User_Address

# Register your models here.

class User_AddressInLine(admin.TabularInline):
    model = User_Address
    extra = 1


class AddressAdmin(admin.ModelAdmin):
    inlines = [User_AddressInLine]


admin.site.register(Address, AddressAdmin)
admin.site.register(User_Address)
