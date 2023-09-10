from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import views as jwt_views

from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer
from .models import CustomUser


class UserCreationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Registration a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    title="Email", type=openapi.TYPE_STRING, format="email",
                    pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})", max_length=255
                ),
                "first_name": openapi.Schema(
                    title="First name", type=openapi.TYPE_STRING,
                    pattern=r"[a-zA-Z]", max_length=255
                ),
                "last_name": openapi.Schema(
                    title="Last name", type=openapi.TYPE_STRING,
                    pattern=r"[a-zA-Z]", max_length=255
                ),
                "partnership_code": openapi.Schema(
                    title="Partnership code", type=openapi.TYPE_STRING,
                    pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})", max_length=100
                ),
                "investment_sector": openapi.Schema(
                    title="Investment sector", type=openapi.TYPE_STRING,
                    pattern=r"[a-zA-Z]", max_length=100
                ),
                "deposit_term": openapi.Schema(
                    title="Deposit term", type=openapi.TYPE_STRING,
                    format="date"
                ),
                "interest_rate": openapi.Schema(
                    title="Interest rate", type=openapi.TYPE_NUMBER,
                    format="float"
                ),
                "password": openapi.Schema(title="Password", type=openapi.TYPE_STRING,
                                           format="password", min_length=8
                                           ),
                "password2": openapi.Schema(
                    title="Password confirmation", type=openapi.TYPE_STRING,
                    format="password", min_length=8
                ),
            },
            required=[
                'email', 'first_name',
                'last_name', 'partnership_code',
                'investment_sector', 'deposit_term',
                'interest_rate', 'password',
                'password2'
            ],
        ),
        responses={201: "Registration is successful", 400: "Bad request - Validation errors!"},
    )
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user = authenticate(email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            login(request, user)

            refresh_token = RefreshToken.for_user(user)

            data = dict()
            data['response'] = "Successfully registered a new user."
            data['refresh'] = str(refresh_token)
            data['access'] = str(refresh_token.access_token)

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DecoratedTokenObtainPairView(jwt_views.TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Token pair getter",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    title="Email", type=openapi.TYPE_STRING, format="email",
                    pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})", max_length=255
                ),
                "password": openapi.Schema(title="Password", type=openapi.TYPE_STRING,
                                           format="password", min_length=8
                                           )
            },
            required=["email", "password"],
        ),
        responses={200: "OK",
                   401: "No active account found with the given credentials"},
    )
    def post(self, request, *args, **kwargs) -> Response:
        user = authenticate(email=request.data['email'],
                            password=request.data['password'])

        if user is not None:
            login(request, user)
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(jwt_views.TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Token pair refresher",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    title="Email", type=openapi.TYPE_STRING, format="email",
                    pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})", max_length=255
                ),
            },
            required=["refresh"],
        ),
        responses={200: "OK",
                   401: "No active account found with the given credentials"},
    )
    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class PersonalCabinetView(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        operation_description="Personal cabinet data getter",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "full_name": openapi.Schema(
                    title="Full name", type=openapi.TYPE_STRING,
                    pattern=r"[a-zA-Z_]", max_length=255
                ),
                "partnership_code": openapi.Schema(
                    title="Partnership code", type=openapi.TYPE_STRING,
                    max_length=100
                ),
                "investment_sector": openapi.Schema(
                    title="Investment sector", type=openapi.TYPE_STRING,
                    pattern=r"[a-zA-Z]", max_length=100
                ),
                "deposit_term": openapi.Schema(
                    title="Deposit term", type=openapi.TYPE_STRING,
                    format="date", pattern=r"(\d{1,2}\/\d{1,2}\/\d{4})"
                ),
                "interest_rate": openapi.Schema(
                    title="Interest rate", type=openapi.TYPE_NUMBER,
                    format="float"
                ),
                "referral_partners_list": openapi.Schema(
                    title="Referral partners", type=openapi.TYPE_ARRAY,
                    items=openapi.TYPE_STRING
                ),
                "total_deposit_amount": openapi.Schema(
                    title="Deposit amount", type=openapi.TYPE_NUMBER,
                    format="float"
                ),
                "received_dividends_amount": openapi.Schema(
                    title="Dividends amount", type=openapi.TYPE_NUMBER,
                    format="float"
                ),
            },
        ),
        responses={200: "OK",
                   401: "Authentication credentials were not provided."},
    )
    def get(self, request, *args, **kwargs) -> Response:
        user = CustomUser.objects.get(id=request.user.id)

        return Response(data={
            "Full name": user.cabinet.full_name,
            "Partnership code": user.cabinet.partnership_code,
            "Investment sector": user.cabinet.investment_sector,
            "Deposit term": user.cabinet.deposit_term,
            "Interest rate": user.cabinet.interest_rate,
            "Referral partners": user.cabinet.referral_partners_list,
            "Deposit amount": user.cabinet.total_deposit_amount,
            "Dividends amount": user.cabinet.received_dividends_amount
        }, status=status.HTTP_200_OK)
