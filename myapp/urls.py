from django.urls import path
from .views import UserCreationView

app_name = 'myapp'

urlpatterns = [
    path('create-user/', UserCreationView.as_view(), name='register'),
]
