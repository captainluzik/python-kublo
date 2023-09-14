from django.urls import path
from .views import (UserCreationView, DecoratedTokenObtainPairView,
                    DecoratedTokenRefreshView, PersonalCabinetView,
                    AllInvestorsView, CabinetUpdateView)

app_name = 'myapp'

urlpatterns = [
    path('create-user/', UserCreationView.as_view(), name='register'),
    path('token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('personal-cabinet/', PersonalCabinetView.as_view(), name='personal_cabinet'),
    path('get-all-investors/', AllInvestorsView.as_view(), name='all_investors'),
    path('cabinet-update/<int:pk>/', CabinetUpdateView.as_view(), name='update_cabinet'),
]
