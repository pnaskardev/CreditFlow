from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from . tasks import calculate_credit_score

from . serializers import CustomerSerializer
from . models import Customer
class RegisterUserApiView(generics.CreateAPIView):
    serializer_class=CustomerSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.data["adhaar_id"])
            calculate_credit_score.delay(serializer.data["adhaar_id"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
