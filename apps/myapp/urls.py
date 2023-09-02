from django.urls import path
from .views import (UserCreationView, CustomTokenObtainPairView,
                    CustomTokenRefreshView)

app_name = 'myapp'

urlpatterns = [
    path('create-user/', UserCreationView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
