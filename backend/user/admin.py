from django.contrib import admin

from . models import Customer, CreditScore

admin.site.register(Customer)
admin.site.register(CreditScore)
