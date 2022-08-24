from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('signup', UserCreateAPIView.as_view(), name='signup'),
    path('login', LogInUser.as_view(), name='login'),
]



