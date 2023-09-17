from django.urls import path, include

from . views import RegisterUserApiView

urlpatterns = [
    path('api/register-user/',RegisterUserApiView.as_view(),name='Customer'),
]
