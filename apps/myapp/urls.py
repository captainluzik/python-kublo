from django.urls import path
from .views import (UserCreationView, DecoratedTokenObtainPairView,
                    DecoratedTokenRefreshView, PersonalCabinetView)

app_name = 'myapp'

urlpatterns = [
    path('create-user/', UserCreationView.as_view(), name='register'),
    path('token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('personal-cabinet/', PersonalCabinetView.as_view(), name='personal_cabinet'),
]
