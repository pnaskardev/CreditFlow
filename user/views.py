from django.shortcuts import render

from rest_framework import generics


from . serializers import CustomerSerializer
from . models import Customer
class RegisterUserApiView(generics.CreateAPIView):
    serializer_class=CustomerSerializer
    queryset=Customer.objects.all()

