from django.contrib import admin

from .models import LoanTypeLimit, LoanApplication

admin.site.register(LoanTypeLimit)
admin.site.register(LoanApplication)
