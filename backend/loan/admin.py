from django.contrib import admin

from .models import LoanApplication, EMI

admin.site.register(LoanApplication)
admin.site.register(EMI)
